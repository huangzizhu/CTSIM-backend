from sqlalchemy import func
from gateway.dao.VisitDaoInterface import VisitDaoInterface
from gateway.orm.OrmEngine import OrmEngine
from gateway.orm.VisitOrm import VisitOrm
from typing import List
from pojo.Visit import VisitCreate, Visit,VisitUpdate

class VisitDaoOrm(VisitDaoInterface):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_inited'):
            super().__init__('visitDaoOrm')
            self.engine = OrmEngine()
            # 保存 Session 工厂
            self.SessionLocal = self.engine.createSessionFactory()
            self._inited = True

    def addVisit(self, visit: VisitCreate) -> Visit:
        session = self.SessionLocal()
        data = visit.dict(exclude_none=True, exclude_unset=True)
        data["updatedTime"] = func.now()
        visitOrm: VisitOrm = VisitOrm(**data)
        try:
            session.add(visitOrm)
            session.commit()
            return Visit.model_validate(visitOrm)
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def getAllVisitsByPid(self, pid: int) -> List[Visit]:
        session = self.SessionLocal()
        try:
            return session.query(VisitOrm).filter(VisitOrm.patientId == pid).all()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def getVisitByPid(self, pid: int) -> Visit | None:
        session = self.SessionLocal()
        try:
            return session.query(VisitOrm).filter(VisitOrm.patientId == pid).order_by(VisitOrm.createdTime.desc()).first()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def updateVisit(self, visit: VisitUpdate) -> int:
        session = self.SessionLocal()
        data = visit.dict(exclude_none=True, exclude_unset=True)
        data["updatedTime"] = func.now()
        data.pop("visitId")
        try:
            rowCount = session.query(VisitOrm).filter(VisitOrm.visitId == visit.visitId).update(data)
            session.commit()
            return rowCount
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def deleteVisitByVisitId(self, visitId: int) -> int:
        session = self.SessionLocal()
        try:
            rowCount = session.query(VisitOrm).filter(VisitOrm.visitId == visitId).delete()
            session.commit()
            return rowCount
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()




