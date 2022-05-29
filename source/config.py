####################################
# Configモジュール
# アプリケーションの設定情報を定義
# 設定情報本体は.envに保持。
####################################

# common modules
import os
from dotenv import load_dotenv


"""
設定クラス
.envからパラメータを取得し、保持する
"""
class Config:
    PATH_DB_INTEGRATION=""

    """
    NAME_SPREADSHEET=""
    PATH_GAUTH_JSON='./gcs_auth.json'

    SHEETNAME_CFG_GAMES="cfg_games"
    SHEETNAME_CFG_DEVICES="cfg_devices"
    SHEETNAME_PATHS="paths"
    SHEETNAME_HISTORIES="histories"
    """

    def __init__(self):
        load_dotenv()

        self.PATH_DB_INTEGRATION = os.environ["PATH_DB_INTEGRATION"] or "./"

    """
        self.NAME_SPREADSHEET = os.environ["NAME_SPREADSHEET"] or "./"
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = self.PATH_GAUTH_JSON
    """