from gateway.dao.ConsultationDaoInterface import ConsultationDaoInterface
from gateway.dao.PatientDaoInterface import PatientDaoInterface
from pojo.Patient import CreatePatient, UpdatePatient, Patient
import sqlite3
from ProjectRoot import getProjectRootPath
from pathlib import Path

class ConsultationDao(ConsultationDaoInterface):
    def __init__(self):
        super().__init__("consultationDao")
        projectRoot = getProjectRootPath()
        self.dbFile: Path = projectRoot.joinpath("ct.db")
        self.chartFile: Path = projectRoot.joinpath("sql/visit.sql")
        with sqlite3.connect(self.dbFile) as con:
            cursor = con.cursor()
            cursor.execute(
                """
                select name from sqlite_master where type='table' and name='visit';
                """
            )
            res = cursor.fetchone()
            if res is None:
                # 创建表
                with open(self.chartFile, "r", encoding="utf-8") as f:
                    sql = f.read()
                    cursor.executescript(sql)
                con.commit()


