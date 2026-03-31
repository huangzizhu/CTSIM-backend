from typing import List
from gateway.dao.CTDaoInterface import CTDaoInterface
from gateway.orm.OrmEngine import OrmEngine
from pojo.CT import CT
from gateway.orm.CTOrm import CTOrm
from gateway.orm.CTOrderOrm import CTOrderOrm
from pojo.CTOrder import CTOrderCreate, CTOrderUpdate, CTOrder


class CTDaoOrm(CTDaoInterface):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_inited'):
            super().__init__("CTDaoOrm")
            self.engine = OrmEngine()
            # 保存 Session 工厂
            self.SessionLocal = self.engine.createSessionFactory()
            self._inited = True

    def getAllCT(self) -> List[CT]:
        session = self.SessionLocal()
        cts = session.query(CTOrm).all()
        session.close()
        return [CT(**ct.__dict__) for ct in cts]

    def addCTOrder(self, order: CTOrderCreate) -> CTOrder:
        session = self.SessionLocal()
        ctOrderOrm = CTOrderOrm(**order.__dict__)
        try:
            session.add(ctOrderOrm)
            session.commit()
            session.refresh(ctOrderOrm)
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
        return CTOrder.model_validate(ctOrderOrm)

    def getAllCTOrdersByPID(self, pid: int) -> List[CTOrder]:
        session = self.SessionLocal()
        try:
            CTOrderOrms: List[CTOrderOrm] = session.query(CTOrderOrm).filter(CTOrderOrm.patientId == pid).all()
            return [CTOrder.model_validate(ctOrderOrm) for ctOrderOrm in CTOrderOrms]
        finally:
            session.close()

    def getNewestCTOrderByPID(self, pid: int) -> CTOrder | None:
        session = self.SessionLocal()
        try:
            ctOrderOrm: CTOrderOrm | None = session.query(CTOrderOrm).filter(CTOrderOrm.patientId == pid).order_by(CTOrderOrm.ordered_at.desc()).first()
            if ctOrderOrm is None:
                return None
            return CTOrder.model_validate(ctOrderOrm)
        finally:
            session.close()

    def getCTOrderByID(self, CtorId: int) -> CTOrder | None:
        session = self.SessionLocal()
        try:
            ctOrderOrm: CTOrderOrm | None = session.query(CTOrderOrm).filter(CTOrderOrm.orderId == CtorId).one_or_none()
            return CTOrder.model_validate(ctOrderOrm)
        finally:
            session.close()


