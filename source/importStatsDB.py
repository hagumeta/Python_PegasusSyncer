import sqlite3
import dataset
import os, stat, datetime

from config import Config
from modules import common
from modules.device import Device
config = Config()

if (not os.path.exists(config.PATH_DB_INTEGRATION)) :
  print ("Integration DB is not initialized!")
  exit(1)

print ("Import And Integrate Pegasus-DB!")
db_integration = dataset.connect(f"sqlite:///{config.PATH_DB_INTEGRATION}")
tb_integration_devices = db_integration["cfg_devices"]
tb_integration_games = db_integration["cfg_games"]
tb_integration_paths = db_integration["paths"]
tb_integration_histories = db_integration["histories"]
nowTime = datetime.datetime.now()


def main (): 
  # デバイス毎に処理を実施する
  for device in tb_integration_devices.find(db_path={'!=': ''}): 
    print (f"device -> {device['name']}")
    deviceCntl = Device(device['db_path'])

    # デバイスDB (デバイス毎の pegasus-stats DB)が最終取り込み時より最新なら接続する
    last_integrated = device['last_integrated'] 
    if (not not last_integrated and
      deviceCntl.get_db_updated_time() < datetime.datetime.strptime(last_integrated, '%Y-%m-%d %H:%M:%S')): 
      print (f"device DB has no update. >> SKIP")
      continue

    # デバイスDB (デバイス毎の pegasus-stats DB)と接続
    original_db = deviceCntl.connect_db()
    if (not original_db):
      print (f"device DB couldnot connect ! => {device['name']} / {device['db_path']} ")
      continue

    # pegasus_frontend出力DBのゲームのうち，未登録のゲームがあれば 統合DBのへ登録
    for path_data in original_db['paths']:
      # game毎のidを取得する．無ければレコードを生成し，取得する
      _fileName = common.getFileName(path_data['path']);
      if tb_integration_games.count(name=_fileName) < 1:
        registerGame(_fileName)
      _game = tb_integration_games.find_one(name=_fileName)
      _gameId = (_game['id'] or -1) if _game else -1

      # ゲームに対応するpathsが無ければレコードを生成し，取得する
      if tb_integration_paths.count(device_id=device['id'], original_path_id=[path_data['id']]) < 1:
        registerPath(device['id'], _gameId, _fileName, path_data['id'], path_data['path'])


    # 統合済のデータの内，最新レコードを取得
    _timeLastPlayed=db_integration.query(
      f"SELECT max(`played_time`) as last_played FROM histories WHERE device_id = {device['id']}"
    ).next()['last_played'] or 0
    # pegasus_frontend出力DBのログから，未登録のログを統合DB`histories`へコピー
    for play in original_db['plays'].find(start_time={'>': _timeLastPlayed}):
      _path = tb_integration_paths.find_one(device_id=device['id'], original_path_id=play['path_id'])
      _pathId = (_path['id'] or -1) if _path else -1
      if _pathId > 0:
        registerHistory(deviceId=device['id'], pathId=_pathId, \
          playedTime=play['start_time'], playedDuration=play['duration'])
    
    original_db.close()

    # デバイス情報の更新をする
    _update = dict(id=device['id'], last_integrated=nowTime.strftime('%Y-%m-%d %H:%M:%S'))
    tb_integration_devices.update(_update, ['id'])
    print ("done.")


# cfg_gamesテーブルに新規レコードを挿入する
def registerGame(_gameName: str):
  _gameData = dict(name=_gameName, label="")
  tb_integration_games.insert(_gameData)

# Pathsテーブルに新規レコードを挿入する
def registerPath(deviceId: str, gameId: str, gameName: str, originalPathId: str, originalPath: str):
  _pathData = dict(device_id=deviceId, game_id=gameId, file_name=gameName, original_path_id=originalPathId, path=originalPath)
  tb_integration_paths.insert(_pathData)

# historiesテーブルに新規レコードを挿入する
def registerHistory(deviceId: str, pathId: str, playedTime: str, playedDuration: str):
  _historyData = dict(device_id=deviceId, path_id=pathId, played_time=playedTime, played_duration=playedDuration)
  tb_integration_histories.insert(_historyData)


main()
db_integration.close()
print ("Import And Integrate Pegasus-DB COMPLETE!")
exit(0)
