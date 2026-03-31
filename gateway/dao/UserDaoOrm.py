# gateway/dao/UserDaoOrm.py
from exceptiongroup import catch

from gateway.dao.UserDaoInterface import UserDaoInterface
from gateway.orm.OrmEngine import OrmEngine
from gateway.orm.UserOrm import UserOrm
from gateway.orm.TokenOrm import RefreshToken
from pojo.User import UserLoginForm, User


class UserDaoOrm(UserDaoInterface):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_inited'):
            super().__init__('userDaoOrm')
            self.engine = OrmEngine()
            # 保存 Session 工厂
            self.SessionLocal = self.engine.createSessionFactory()
            self._inited = True

    def login(self, userLoginForm: UserLoginForm) -> User | None:
        """
        使用 ORM 查询 user 表，入参是 Pydantic 的 UserLoginForm，
        返回 Pydantic 的 User（或 None）。
        """
        session = self.SessionLocal()
        try:
            dbUser: UserOrm | None = (
                session.query(UserOrm)
                .filter(UserOrm.username == userLoginForm.username)
                .first()
            )
            if dbUser is None:
                return None

            return User(
                userId=dbUser.uid,
                username=dbUser.username,
                hashedPassword=dbUser.hashedPassword,
                level=dbUser.level,
            )
        finally:
            session.close()

    def deleteTokensByUserId(self, userId: int):
        """
        删除某个用户的所有 refresh_tokens 记录。
        """
        session = self.SessionLocal()
        try:
            (
                session.query(RefreshToken)
                .filter(RefreshToken.userId == userId)
                .delete(synchronize_session=False)
            )
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def insertTokens(self, userId: int, newToken: str):
        """
        插入一条 refresh_tokens 记录。
        这里沿用原接口：传 userId 和 refreshToken 字符串。
        """
        session = self.SessionLocal()
        try:
            token = RefreshToken(
                userId=userId,
                refreshToken=newToken,
            )
            session.add(token)
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def checkRefreshToken(self, refreshToken: str) -> int | None:
        """
        检查 refreshToken 是否存在，存在则返回 userId，不存在返回 None。
        """
        session = self.SessionLocal()
        try:
            dbToken: RefreshToken | None = (
                session.query(RefreshToken)
                .filter(RefreshToken.refreshToken == refreshToken)
                .first()
            )
            if dbToken is None:
                return None
            return dbToken.userId
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def getUserByUid(self, uid: int) -> User | None:
        session = self.SessionLocal()
        try:
            dbUser: UserOrm | None = (
                session.query(UserOrm)
                .filter(UserOrm.uid == uid)
                .one_or_none()
            )
            if dbUser is not None:
                return User(**{
                    **dbUser.__dict__,
                    "userId": dbUser.uid,
                })
            else:
                return None
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
