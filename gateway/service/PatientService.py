from typing import List

from Exception.DataBaseException import DataBaseException
from Exception.PatientNotFoundException import PatientNotFoundException
from gateway.dao.PatientDaoInterface import PatientDaoInterface
from gateway.dao.PatientDaoWithSqlLite import PatientDaoWithSqlLite
from pojo.Patient import CreatePatient, UpdatePatient,Patient
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
            countRows: int = self.patientDao.updatePatient(patient)
        except SQLiteError as e:
            raise DataBaseException(e.args[0])
        if countRows == 0:
            raise PatientNotFoundException(f"Patient {patient.pid} not found")

    def getAllPatients(self) -> List[Patient]:
        try:
            patients: List[Patient] = self.patientDao.getAllPatients()
        except SQLiteError as e:
            raise DataBaseException(e.args[0])
        return patients

    def deletePatient(self, pid):
        try:
            countRows: int = self.patientDao.deletePatient(pid)
        except SQLiteError as e:
            raise DataBaseException(e.args[0])
        if countRows == 0:
            raise PatientNotFoundException(f"Patient pid = {pid} not found")








