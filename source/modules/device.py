from copyreg import constructor
import os, datetime
import shutil
import dataset


class Device: 
  path: str;

  def __init__(self, base_path: str): 
    self.path = base_path
  
  def get_db_path (self): 
    return f"{self.path}\stats.db"

  def get_backup_path (self): 
    return f"{self.path}\\backup"

  def is_db_exists (self): 
    return os.path.exists(self.get_db_path())


  def connect_db (self) : 
    if (not self.is_db_exists()):
      return None
    return dataset.connect(f"sqlite:///{self.get_db_path()}")

  def get_db_updated_time (self) : 
    if (not self.is_db_exists()):
      return None
    return datetime.datetime.fromtimestamp(os.path.getmtime(self.get_db_path()))

  def create_db_backup (self): 
    time=datetime.datetime.now().strftime('%Y-%m-%d_%H-%M')
    backup_path = f"{self.get_backup_path()}\stats_{time}.db"
    shutil.copy(self.get_db_path(), backup_path)
