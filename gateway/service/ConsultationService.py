from typing import List

from Exception.DataBaseException import DataBaseException
from Exception.PatientNotFoundException import PatientNotFoundException
from gateway.dao.PatientDaoInterface import PatientDaoInterface
from gateway.dao.PatientDaoWithSqlLite import PatientDaoWithSqlLite
from pojo.Patient import CreatePatient, UpdatePatient,Patient
from sqlite3 import Error as SQLiteError

class ConsultationService:
    def __init__(self):
        self