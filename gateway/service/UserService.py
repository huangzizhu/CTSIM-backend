from Exception.DataBaseException import DataBaseException
from Exception.InvalidTokenError import InvalidTokenError
from Exception.PasswordIncorrectException import PasswordIncorrectException
from Exception.TokenExpiredException import TokenExpiryException
from gateway.dao.UserDaoWithSqlLite import UserDaoWithSqlLite
from gateway.dao.UserDaoInterface import UserDaoInterface
from pojo.Tokens import Tokens
from pojo.User import UserLoginForm,User
from utils.JWTTokenTool import generateTokens,refreshAccessToken
from Exception.UserNotFoundException import UserNotFoundException
from sqlite3 import Error as SQLiteError


class UserService():
    def __init__(self):
        self.userDao: UserDaoInterface = UserDaoWithSqlLite()

    def login(self, userLoginForm: UserLoginForm):
        try:
            user: User = self.userDao.login(userLoginForm)
        except SQLiteError as e:
            raise DataBaseException(e.args[0])
        if user:
            if user.hashedPassword == userLoginForm.hashedPassword:
                # 登陆成功
                # 生成token
                newToken: Tokens = generateTokens(user.userId)
                try:
                    # 删除旧token
                    self.userDao.deleteTokensByUserId(user.userId)
                    # 存储新token
                    self.userDao.insertTokens(user.userId, newToken.refreshToken)
                except SQLiteError as e:
                    raise DataBaseException(e.args[0])
                return newToken
            raise PasswordIncorrectException()
        raise UserNotFoundException("No user ")

    def logout(self, userId: int):
        try:
            self.userDao.deleteTokensByUserId(userId)
        except SQLiteError as e:
            raise DataBaseException(e.args[0])


    def refresh(self, token: Tokens) -> Tokens:
        try:
            userId: int = self.userDao.checkRefreshToken(token.refreshToken)
        except SQLiteError as e:
            raise DataBaseException(e.args[0])

        # 这里的token是前端传来的refreshToken
        res = refreshAccessToken(token.refreshToken)
        #uid有效，但是过期了
        if userId is None and res[1] :
            raise TokenExpiryException()
        # 确保check出来的userid和refresh token里的一样
        if res[1] != userId:
            raise InvalidTokenError("The token does not match the user")
        token.accessToken = res[0]
        return token








