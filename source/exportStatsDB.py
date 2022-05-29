import sqlite3
import dataset
import os, stat, datetime
from datetime import timedelta

from config import Config
from modules import common
from modules.device import Device
config = Config()

if (not os.path.exists(config.PATH_DB_INTEGRATION)) :
  print ("Integration DB is not initialized!")
  exit(1)

print ("Export Pegasus-DB!")
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

    # pegasus_frontend出力DBの更新が10分以内の場合，更新しない
#    if deviceCntl.get_db_updated_time() > (nowTime + timedelta(minutes=-10)):
#      print (f"device DB is using now. cant update. >> SKIP")
#      continue

    # バックアップを作成する
    deviceCntl.create_db_backup()

    # デバイスDB (デバイス毎の pegasus-stats DB)と接続
    original_db = deviceCntl.connect_db()
    if (not original_db):
      print (f"device DB couldnot connect ! => {device['name']} / {device['db_path']} ")
      continue
    original_db.begin()


    # DBのデータ削除
    original_db['plays'].delete()

    # 統合DBから，デバイス内で定義されたゲーム履歴を取得し，インサートする
    insertPlays = []
    for path in tb_integration_paths.find(device_id=device['id']):
      insertPlays.extend(\
        list(
          map(
            lambda history:  {\
                "start_time": history['played_time'], \
                "duration": history['played_duration'], \
                "path_id": history['original_path_id']\
              }, \
            tb_integration_histories.find(path_id=path['id'])
          )
        )
      )
    insertPlays.sort(key=lambda x: x['start_time'])

    original_db['plays'].insert_many(insertPlays)
    original_db.commit()
    original_db.close()

    print ('done!')


main()
db_integration.close()
print ("Export Pegasus-DB COMPLETE!")
exit(0)
