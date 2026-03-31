from typing import List
from Exception.DataBaseException import DataBaseException
from gateway.dao.PatientDaoInterface import PatientDaoInterface
from gateway.dao.CTDaoInterface import CTDaoInterface
from gateway.dao.CTDaoOrm import CTDaoOrm
from gateway.dao.PatientDaoOrm import PatientDaoOrm
from pojo.CT import CT
from pojo.CTOrder import CTOrderCreate,CTOrderUpdate,CTOrder
from gateway.service.ServiceUtils import checkPatient
from Exception.CTOrderNotFoundException import CTOrderNotFoundException

class CTService:
    def __init__(self):
        self.CTDao : CTDaoInterface = CTDaoOrm()
        self.patientDao : PatientDaoInterface = PatientDaoOrm()

    def getAllCT(self) -> List[CT]:
        try:
            return self.CTDao.getAllCT()
        except Exception as e:
            raise DataBaseException(e.args[0])

    def addCTOrder(self, order: CTOrderCreate) -> CTOrder:
        try:
            return self.CTDao.addCTOrder(order)
        except Exception as e:
            raise DataBaseException(e.args[0])

    def  getAllCTOrdersByPID(self, pid: int) -> List[CTOrder]:
        checkPatient(pid,self.patientDao)
        try:
            return self.CTDao.getAllCTOrdersByPID(pid)
        except Exception as e:
            raise DataBaseException(e.args[0])

    def getNewestCTOrderByPID(self, pid: int) -> CTOrder | None:
        checkPatient(pid, self.patientDao)
        try:
            return self.CTDao.getNewestCTOrderByPID(pid)
        except Exception as e:
            raise DataBaseException(e.args[0])

    def getCTOrderByID(self, CtorId: int) -> CTOrder:
        try:
            ctOrder: CTOrder | None = self.CTDao.getCTOrderByID(CtorId)
            if ctOrder is None:
                raise CTOrderNotFoundException(f"CTOrder CTOrderId={CtorId} not found")
            return ctOrder
        except Exception as e:
            raise DataBaseException(e.args[0])

