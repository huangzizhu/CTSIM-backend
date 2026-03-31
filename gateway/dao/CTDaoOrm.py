from typing import List
from gateway.dao.CTDaoInterface import CTDaoInterface
from gateway.orm.OrmEngine import OrmEngine
from pojo.CT import CT
from gateway.orm.CTOrm import CTOrm
from gateway.orm.CTOrderOrm import CTOrderOrm
from pojo.CTOrder import CTOrderCreate,CTOrderUpdate,CTOrder

class CTDaoOrm(CTDaoInterface):
    def __init__(self):
        super().__init__("CTDaoOrm")
        self.engine = OrmEngine()
        # 保存 Session 工厂
        self.SessionLocal = self.engine.createSessionFactory()

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


