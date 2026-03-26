from gateway.dao.PatientDaoInterface import PatientDaoInterface
from gateway.dao.PatientDaoWithSqlLite import PatientDaoWithSqlLite

class PatientService:
    def __init__(self):
        self.patientDao: PatientDaoInterface = PatientDaoWithSqlLite()

