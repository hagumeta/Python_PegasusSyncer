from distutils.command.config import config
from genericpath import exists
from inspect import _void
import sqlite3
import _sqlite3
import os, stat
from config import Config

config = Config()

if (os.path.exists(config.PATH_DB_INTEGRATION)) :
  print ("Integration DB is already initialized!")
  exit(1)

db = sqlite3.connect(
    config.PATH_DB_INTEGRATION,
    isolation_level=None,
)

sql1 = """
    CREATE TABLE cfg_games (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        label TEXT
    );
"""
sql2 = """
    CREATE TABLE cfg_devices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        db_path TEXT
    );
"""
sql3 = """
    CREATE TABLE paths (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        device_id INTEGER,
        game_id INTEGER,
        original_path_id INTEGER,
        path TEXT,
        file_name TEXT
    );
"""
sql4 = """
    CREATE TABLE histories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        device_id INTEGER,
        path_id INTEGER,
        game_id INTEGER,
        played_time INTEGER,
        played_duration INTEGER
    );
"""

db.execute(sql1)
db.execute(sql2)
db.execute(sql3)
db.execute(sql4)
db.close()