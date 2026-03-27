

from Exception.DataBaseException import DataBaseException
from gateway.dao.PatientDaoInterface import PatientDaoInterface
from gateway.dao.PatientDaoWithSqlLite import PatientDaoWithSqlLite
from pojo.Patient import CreatePatient, UpdatePatient
from sqlite3 import Error as SQLiteError

class PatientService:
    def __init__(self):
        self.patientDao: PatientDaoInterface = PatientDaoWithSqlLite()

    def addPatient(self, patient: CreatePatient):
        try:
            self.patientDao.addPatient(patient)
        except SQLiteError as e:
            raise DataBaseException(e.args[0])

    def updatePatient(self, patient: UpdatePatient):
        try:
            self.patientDao.updatePatient(patient)
        except SQLiteError as e:
            raise DataBaseException(e.args[0])







