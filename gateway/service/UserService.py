from Exception.InvalidTokenError import InvalidTokenError
from Exception.PasswordIncorrectException import PasswordIncorrectException
from Exception.TokenExpiredException import TokenExpiryException
from gateway.dao.UserDaoWithSqlLite import UserDaoWithSqlLite
from gateway.dao.UserDaoInterface import UserDaoInterface
from pojo.Tokens import Tokens
from pojo.User import UserLoginForm,User
from utils.JWTTokenTool import generateTokens,refreshAccessToken
from Exception.UserNotFoundException import UserNotFoundException


class UserService():
    def __init__(self):
        self.userDao: UserDaoInterface = UserDaoWithSqlLite()

    def login(self, userLoginForm: UserLoginForm):
        user: User = self.userDao.login(userLoginForm)
        if user:
            if user.hashedPassword == userLoginForm.hashedPassword:
                # 登陆成功
                # 生成token
                newToken: Tokens = generateTokens(user.userId)
                # 删除旧token
                self.userDao.deleteTokensByUserId(user.userId)
                # 存储新token
                self.userDao.insertTokens(user.userId, newToken.refreshToken)
                return newToken
            raise PasswordIncorrectException()
        raise UserNotFoundException("No user ")

    def logout(self, userId: int):
        self.userDao.deleteTokensByUserId(userId)

    def refresh(self, token: Tokens) -> Tokens:
        userId: int = self.userDao.checkRefreshToken(token.refreshToken)
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








