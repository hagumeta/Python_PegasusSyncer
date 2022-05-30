
from time import sleep

# インポート処理実行
exec(open('importStatsDB.py').read())
sleep(1)

# エクスポート処理実行
exec(open('exportStatsDB.py').read())
exit (0)
