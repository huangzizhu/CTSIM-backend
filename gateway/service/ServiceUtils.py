from gateway.dao.PatientDaoInterface import PatientDaoInterface
from gateway.dao.UserDaoInterface import UserDaoInterface
from gateway.dao.CTDaoInterface import CTDaoInterface
from gateway.dao.VisitDaoInterface import VisitDaoInterface
from pojo.User import User
from pojo.Patient import Patient
from pojo.Visit import Visit
from pojo.CT import CT
from Exception.PatientNotFoundException import PatientNotFoundException
from Exception.UserNotFoundException import UserNotFoundException
from Exception.DataBaseException import DataBaseException
from Exception.VisitNotFoundException import VisitNotFoundException
from Exception.CTNotFoundException import CTNotFoundException


def checkUser(uid: int,userDao: UserDaoInterface):
    try:
        user: User = userDao.getUserByUid(uid)
    except Exception as e:
        raise DataBaseException(str(e))
    if not user:
        raise UserNotFoundException(f"User uid={uid} not found")


def checkPatient(pid: int, patientDao: PatientDaoInterface):
    # 检查pid是否存在
    try:
        patient: Patient = patientDao.getPatientById(pid)
    except Exception as e:
        raise DataBaseException(str(e))
    if not patient:
        raise PatientNotFoundException(f"Patient pid={pid} not found")

def checkVisitId(visitId: int, visitDao: VisitDaoInterface):
    try:
        visit: Visit = visitDao.getVisitByPid(visitId)
    except Exception as e:
        raise DataBaseException(str(e))
    if not visit:
        raise VisitNotFoundException(f"Visit visitId={visitId} not found")


def checkCTId(ctId: int, ctDao: CTDaoInterface):
    try:
        ct: CT = ctDao.getCTByCTId(ctId)
    except Exception as e:
        raise DataBaseException(str(e))
    if not ct:
        raise CTNotFoundException(f"CT ctId={ctId} not found")

def checkCTOrder(orderId: int, ctDao: CTDaoInterface):
    pass