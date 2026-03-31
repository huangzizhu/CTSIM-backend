from gateway.dao.UserDaoInterface import UserDaoInterface
from gateway.dao.UserDaoOrm import UserDaoOrm
from gateway.dao.VisitDaoInterface import VisitDaoInterface
from gateway.dao.PatientDaoInterface import PatientDaoInterface
from gateway.dao.PatientDaoOrm import PatientDaoOrm
from gateway.dao.VisitDaoOrm import VisitDaoOrm
from Exception.DataBaseException import DataBaseException
from Exception.VisitNotFoundException import VisitNotFoundException
from pojo.Visit import VisitCreate,Visit,VisitUpdate
from typing import List
from gateway.service.ServiceUtils import checkPatient, checkUser


class VisitService:
    def __init__(self):
        self.visitDao: VisitDaoInterface = VisitDaoOrm()
        self.patientDao: PatientDaoInterface = PatientDaoOrm()
        self.userDao: UserDaoInterface = UserDaoOrm()

    def addVisit(self, visit: VisitCreate):
        checkPatient(visit.patientId,self.patientDao)
        checkUser(visit.doctorId,self.userDao)
        try:
            return self.visitDao.addVisit(visit)
        except Exception as e:
            raise DataBaseException(e.args[0])

    def getAllVisitsByPid(self, pid: int) -> List[Visit]:
        checkPatient(pid,self.patientDao)
        #根据pid查询所有就诊记录
        try:
            return self.visitDao.getAllVisitsByPid(pid)
        except Exception as e:
            raise DataBaseException(e.args[0])

    def getVisitByPid(self, pid):
        checkPatient(pid,self.patientDao)
        #根据pid查询最新就诊记录
        try:
            return self.visitDao.getVisitByPid(pid)
        except Exception as e:
            raise DataBaseException(e.args[0])

    def updateVisit(self, visit: VisitUpdate) -> Visit | None:
        # 更新就诊记录
        if visit.patientId is not None:
            checkPatient(visit.patientId,self.patientDao)
        if visit.doctorId is not None:
            checkUser(visit.doctorId,self.userDao)
        try:
            rowCount: int = self.visitDao.updateVisit(visit)
            if rowCount == 0:
                raise VisitNotFoundException(f"Visit visitId={visit.visitId} not found")
        except Exception as e:
            raise DataBaseException(e.args[0])
        # 回显
        try:
            return self.visitDao.getVisitByPid(visit.visitId)
        except Exception as e:
            raise DataBaseException(e.args[0])


    def deleteVisitByVisitId(self, visitId: int):
        try:
            rowCount: int = self.visitDao.deleteVisitByVisitId(visitId)
            if rowCount == 0:
                raise VisitNotFoundException(f"Visit visitId={visitId} not found")
        except Exception as e:
            raise DataBaseException(e.args[0])









