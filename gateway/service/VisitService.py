from gateway.dao.UserDaoInterface import UserDaoInterface
from gateway.dao.UserDaoOrm import UserDaoOrm
from gateway.dao.VisitDaoInterface import VisitDaoInterface
from gateway.dao.PatientDaoInterface import PatientDaoInterface
from gateway.dao.PatientDaoOrm import PatientDaoOrm
from gateway.dao.VisitDaoOrm import VisitDaoOrm
from Exception.DataBaseException import DataBaseException
from Exception.PatientNotFoundException import PatientNotFoundException
from Exception.VisitNotFoundException import VisitNotFoundException
from Exception.UserNotFoundException import UserNotFoundException
from pojo.Visit import VisitCreate,Visit,VisitUpdate
from pojo.User import User
from pojo.Patient import Patient
from typing import List


class VisitService:
    def __init__(self):
        self.visitDao: VisitDaoInterface = VisitDaoOrm()
        self.patientDao: PatientDaoInterface = PatientDaoOrm()
        self.userDao: UserDaoInterface = UserDaoOrm()

    def addVisit(self, visit: VisitCreate):
        self.checkPatient(visit.patientId)
        self.checkUser(visit.doctorId)
        try:
            self.visitDao.addVisit(visit)
        except Exception as e:
            raise DataBaseException(e.args[0])

    def getAllVisitsByPid(self, pid: int) -> List[Visit]:
        self.checkPatient(pid)
        #根据pid查询所有就诊记录
        try:
            return self.visitDao.getAllVisitsByPid(pid)
        except Exception as e:
            raise DataBaseException(e.args[0])

    def getVisitByPid(self, pid):
        self.checkPatient(pid)
        #根据pid查询最新就诊记录
        try:
            return self.visitDao.getVisitByPid(pid)
        except Exception as e:
            raise DataBaseException(e.args[0])

    def updateVisit(self, visit: VisitUpdate):
        if visit.patientId is not None:
            self.checkPatient(visit.patientId)
        if visit.doctorId is not None:
            self.checkUser(visit.doctorId)
        try:
            rowCount: int = self.visitDao.updateVisit(visit)
            if rowCount == 0:
                raise VisitNotFoundException(f"Visit visitId={visit.visitId} not found")
        except Exception as e:
            raise DataBaseException(e.args[0])

    def deleteVisitByVisitId(self, visitId: int):
        try:
            rowCount: int = self.visitDao.deleteVisitByVisitId(visitId)
            if rowCount == 0:
                raise VisitNotFoundException(f"Visit visitId={visitId} not found")
        except Exception as e:
            raise DataBaseException(e.args[0])


    def checkUser(self, uid: int):
        try:
            user: User = self.userDao.getUserByUid(uid)
        except Exception as e:
            raise DataBaseException(e.args[0])
        if not user:
            raise UserNotFoundException(f"User uid={uid} not found")


    def checkPatient(self, pid: int):
        # 检查pid是否存在
        try:
            patient: Patient = self.patientDao.getPatientById(pid)
        except Exception as e:
            raise DataBaseException(e.args[0])
        if not patient:
            raise PatientNotFoundException(f"Patient pid={pid} not found")






