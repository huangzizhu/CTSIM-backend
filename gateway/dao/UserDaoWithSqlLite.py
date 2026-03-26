import sqlite3
from datetime import time
from typing import Any

from gateway.dao.UserDaoInterface import UserDaoInterface
from pojo.User import UserLoginForm, User
from ProjectRoot import getProjectRootPath
from pathlib import Path


class UserDaoWithSqlLite(UserDaoInterface):
    def __init__(self):
        super().__init__("userDao")
        projectRoot = getProjectRootPath()
        self.dbFile: Path = projectRoot.joinpath("ct.db")
        self.chartFile: Path = projectRoot.joinpath("sql/user.sql")
        with sqlite3.connect(self.dbFile) as con:
            cursor = con.cursor()
            cursor.execute(
                """
                select name from sqlite_master where type='table' and name='user';
                """
            )
            res = cursor.fetchone()
            if res is None:
                #创建表
                with open(self.chartFile, "r", encoding="utf-8") as f:
                    sql = f.read()
                    cursor.executescript(sql)
                con.commit()


    def login(self, userLoginForm: UserLoginForm) -> User | None:
        with sqlite3.connect(self.dbFile) as con:
            cursor = con.cursor()
            cursor.execute(
                """
                select * from user where username = ?
                """,
                (userLoginForm.username,),
            )
            res = cursor.fetchone()
            if res:
                return User(
                    userId=res[0],
                    username=res[1],
                    hashedPassword=res[2],
                    level=res[3]
                )
            return None

    def deleteTokensByUserId(self, userId):
        with sqlite3.connect(self.dbFile) as con:
            cursor = con.cursor()
            cursor.execute(
                """
                delete from refresh_tokens where userId = ?
                """,
                (userId,),
            )
            con.commit()

    def insertTokens(self, userId, newToken: str):
        with sqlite3.connect(self.dbFile) as con:
            cursor = con.cursor()
            cursor.execute(
                """
                insert into refresh_tokens (userId, refreshToken) values (?, ?)
                """,
                (userId, newToken ),
            )
            con.commit()

    def checkRefreshToken(self, refreshToken) -> int | None:
        with sqlite3.connect(self.dbFile) as con:
            cursor = con.cursor()
            cursor.execute(
                """
                select userId from refresh_tokens where refreshToken = ?
                """,
                (refreshToken, ),
            )
            res = cursor.fetchone()
            if res:
                return res[0]
            return None



if __name__ == '__main__':
    userDao = UserDaoWithSqlLite()
    print(userDao.chartFile)
    with open(userDao.chartFile, "r", encoding="utf-8") as f:
        sql = f.read()
        print(sql)
