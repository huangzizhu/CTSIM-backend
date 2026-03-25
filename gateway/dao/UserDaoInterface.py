from gateway.dao.UserDaoWithSqlLite import UserDao
from abc import ABC, abstractmethod

from pojo.User import UserLoginForm


class UserDaoInterface(ABC):
    def __init__(self,name: str):
        self.name = name

    @abstractmethod
    def login(self, userLoginForm: UserLoginForm):
        pass
