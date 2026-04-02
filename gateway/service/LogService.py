from typing import List
from gateway.dao.LogDaoInterface import LogDaoInterface
from gateway.dao.LogDaoOrm import LogDaoOrm
from pojo.Log import Log
from Exception.DataBaseException import DataBaseException



class LogService:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_inited'):
            self.logDao: LogDaoInterface = LogDaoOrm()


    def insertLog(self,log: Log):
        try:
            self.logDao.insertLog(log)
        except Exception:
            pass

    def getAllLogs(self) -> List[Log]:
        try:
            return self.logDao.getAllLogs()
        except Exception as e:
            raise DataBaseException(str(e))


