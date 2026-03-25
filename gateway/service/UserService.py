from gateway.dao.UserDaoWithSqlLite import UserDaoWithSqlLite
from gateway.dao.UserDaoInterface import UserDaoInterface
from pojo.User import UserLoginForm


class UserService():
    def __init__(self):
        self.userDao: UserDaoInterface = UserDaoWithSqlLite()

    def login(self, userLoginForm: UserLoginForm):
        isValiad : bool = self.userDao.login(userLoginForm)


