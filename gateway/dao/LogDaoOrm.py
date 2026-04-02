from gateway.dao.LogDaoInterface import LogDaoInterface
from gateway.orm.OrmEngine import OrmEngine
from pojo.Log import Log
from gateway.orm.LogOrm import LogOrm
from typing import List

class LogDaoOrm(LogDaoInterface):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_inited'):
            super().__init__('logDaoOrm')
            self.engine = OrmEngine()
            # 保存 Session 工厂
            self.SessionLocal = self.engine.createSessionFactory()
            self._inited = True


    def insertLog(self, log: Log):
        session = self.SessionLocal()
        logOrm: LogOrm = LogOrm(**Log.model_dump(log,exclude_none=True,exclude_unset=True))
        try:
            session.add(logOrm)
            session.commit()
        except Exception as e:
            session.rollback()
            raise
        finally:
            session.close()

    def getAllLogs(self) -> List[Log]:
        session = self.SessionLocal()
        try:
            logOrms: List[LogOrm] = session.query(LogOrm).all()
            return [Log.model_validate(logOrm) for logOrm in logOrms]
        except Exception:
            raise
        finally:
            session.close()
