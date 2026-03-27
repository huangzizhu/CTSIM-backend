from abc import ABC, abstractmethod
from typing import List
from pojo.Patient import Patient
from gateway.dao.UserDaoInterface import UserDaoInterface
from pojo.User import UserLoginForm, User
from ProjectRoot import getProjectRootPath
from pathlib import Path


class PatientDaoInterface(ABC):
    def __init__(self,name: str):
        self.name = name

    @abstractmethod
    def addPatient(self, patient):
        pass

    @abstractmethod
    def updatePatient(self, patient) -> int:
        pass

    @abstractmethod
    def getAllPatients(self) -> List[Patient]:
        pass

    @abstractmethod
    def deletePatient(self, pid) -> int:
        pass