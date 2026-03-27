from abc import ABC, abstractmethod
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
    def updatePatient(self, patient):
        pass