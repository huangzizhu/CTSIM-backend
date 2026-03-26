import sqlite3
from gateway.dao.UserDaoInterface import UserDaoInterface
from pojo.User import UserLoginForm
from utils import getProjectRootPath
from pathlib import Path

class UserDaoWithSqlLite(UserDaoInterface):
    def __init__(self):
        super().__init__("userDao")
        projectRoot = getProjectRootPath()
        self.dbFile: Path = projectRoot.joinpath("ct.db")
        self.chartFile: Path = projectRoot.joinpath("sql\\user.sql")
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


    def login(self, userLoginForm: UserLoginForm):
        with sqlite3.connect(self.dbFile) as con:
            cursor = con.cursor()
            cursor.execute(
                """
                select * from user where username = ? and hashedPassword = ?
                """,
                (userLoginForm.username, userLoginForm.hashedPassword),
            )


if __name__ == '__main__':
    userDao = UserDaoWithSqlLite()
    print(userDao.chartFile)
    with open(userDao.chartFile, "r", encoding="utf-8") as f:
        sql = f.read()
        print(sql)
