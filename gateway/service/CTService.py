from typing import List
from Exception.DataBaseException import DataBaseException
from gateway.dao.PatientDaoInterface import PatientDaoInterface
from gateway.dao.CTDaoInterface import CTDaoInterface
from gateway.dao.VisitDaoInterface import VisitDaoInterface
from gateway.dao.VisitDaoOrm import VisitDaoOrm

from gateway.dao.CTDaoOrm import CTDaoOrm
from gateway.dao.PatientDaoOrm import PatientDaoOrm
from pojo.CT import CT
from pojo.CTOrder import CTOrderCreate,CTOrderUpdate,CTOrder
from gateway.service.ServiceUtils import checkPatient,checkVisitId,checkCTId
from Exception.CTOrderNotFoundException import CTOrderNotFoundException

class CTService:
    def __init__(self):
        self.CTDao : CTDaoInterface = CTDaoOrm()
        self.patientDao : PatientDaoInterface = PatientDaoOrm()
        self.visitDao : VisitDaoInterface= VisitDaoOrm()

    def getAllCT(self) -> List[CT]:
        try:
            return self.CTDao.getAllCT()
        except Exception as e:
            raise DataBaseException(str(e))

    def addCTOrder(self, order: CTOrderCreate) -> CTOrder:
        checkPatient(order.patientId,self.patientDao)
        checkVisitId(order.visitId,self.visitDao)
        checkCTId(order.ctId,self.CTDao)

        try:
            return self.CTDao.addCTOrder(order)
        except Exception as e:
            raise DataBaseException(str(e))

    def  getAllCTOrdersByPID(self, pid: int) -> List[CTOrder]:
        checkPatient(pid,self.patientDao)
        try:
            return self.CTDao.getAllCTOrdersByPID(pid)
        except Exception as e:
            raise DataBaseException(str(e))

    def getNewestCTOrderByPID(self, pid: int) -> CTOrder | None:
        checkPatient(pid, self.patientDao)
        try:
            return self.CTDao.getNewestCTOrderByPID(pid)
        except Exception as e:
            raise DataBaseException(str(e))

    def getCTOrderByID(self, CtorId: int) -> CTOrder:
        try:
            ctOrder: CTOrder | None = self.CTDao.getCTOrderByID(CtorId)
            if ctOrder is None:
                raise CTOrderNotFoundException(f"CTOrder CTOrderId={CtorId} not found")
            return ctOrder
        except Exception as e:
            raise DataBaseException(str(e))

    def updateOrder(self, order: CTOrderUpdate) -> CTOrder | None:
        try:
            rowCount: int = self.CTDao.updateOrder(order)
        except Exception as e:
            raise DataBaseException(str(e))
        if rowCount == 0:
            raise CTOrderNotFoundException(f"CTOrder CTOrderId={order.orderId} not found")
        return self.CTDao.getCTOrderByID(order.orderId)

    def cancelOrder(self, orderId: int) -> None:
        pass


