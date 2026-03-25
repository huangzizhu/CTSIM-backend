import os
import sqlite3

from UserDaoInterface import UserDaoInterface
from pojo.User import UserLoginForm


class UserDaoWithSqlLite(UserDaoInterface):
    def __init__(self):
        self.dbFile: str = 'ct.db'
        self.chartFile: str = ''
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
                #with open()
                pass

        super().__init__("userDao")

    def login(self, userLoginForm: UserLoginForm):
        pass


if __name__ == '__main__':
    print(os.getcwd())
