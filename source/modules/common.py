import os

def getFileName(path: str): 
  _fileName = os.path.splitext(path)[0]
  if not('android:com' in _fileName or 'android:org' in _fileName):
    _fileName = os.path.splitext(_fileName)[0]
  return _fileName
