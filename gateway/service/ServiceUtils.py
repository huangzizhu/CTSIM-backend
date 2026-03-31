from gateway.dao.PatientDaoInterface import PatientDaoInterface
from gateway.dao.UserDaoInterface import UserDaoInterface
from pojo.User import User
from pojo.Patient import Patient
from Exception.PatientNotFoundException import PatientNotFoundException
from Exception.UserNotFoundException import UserNotFoundException
from Exception.DataBaseException import DataBaseException


def checkUser(uid: int,userDao: UserDaoInterface):
    try:
        user: User = userDao.getUserByUid(uid)
    except Exception as e:
        raise DataBaseException(e.args[0])
    if not user:
        raise UserNotFoundException(f"User uid={uid} not found")


def checkPatient(pid: int, patientDao: PatientDaoInterface):
    # 检查pid是否存在
    try:
        patient: Patient = patientDao.getPatientById(pid)
    except Exception as e:
        raise DataBaseException(e.args[0])
    if not patient:
        raise PatientNotFoundException(f"Patient pid={pid} not found")