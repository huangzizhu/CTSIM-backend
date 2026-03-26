from abc import ABC, abstractmethod

from pojo.User import UserLoginForm, User


class UserDaoInterface(ABC):
    def __init__(self,name: str):
        self.name = name

    @abstractmethod
    def login(self, userLoginForm: UserLoginForm) -> User:
        pass

    @abstractmethod
    def deleteTokensByUserId(self, userId):
        pass

    @abstractmethod
    def insertTokens(self, userId, newToken):
        pass

    @abstractmethod
    def checkRefreshToken(self, refreshToken):
        pass

