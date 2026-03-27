
from gateway.dao.PatientDaoInterface import PatientDaoInterface
from pojo.Patient import CreatePatient, UpdatePatient
import sqlite3
from ProjectRoot import getProjectRootPath
from pathlib import Path

class PatientDaoWithSqlLite(PatientDaoInterface):
    def __init__(self):
        super().__init__("patientDao")
        projectRoot = getProjectRootPath()
        self.dbFile: Path = projectRoot.joinpath("ct.db")
        self.chartFile: Path = projectRoot.joinpath("sql/refreshToken.sql")
        with sqlite3.connect(self.dbFile) as con:
            cursor = con.cursor()
            cursor.execute(
                """
                select name from sqlite_master where type='table' and name='refresh_tokens';
                """
            )
            res = cursor.fetchone()
            if res is None:
                # 创建表
                with open(self.chartFile, "r", encoding="utf-8") as f:
                    sql = f.read()
                    cursor.executescript(sql)
                con.commit()

    def addPatient(self, patient: CreatePatient):
        with sqlite3.connect(self.dbFile) as con:
            cursor = con.cursor()
            # 插入病人数据的 SQL 语句
            sql = '''
                        INSERT INTO patients (
                            cardNo,
                            name,
                            gender,
                            birthDate,
                            phone,
                            idNumber,
                            address,
                            emergencyContactName,
                            emergencyContactPhone,
                            createdTime,
                            updatedTime
                        ) VALUES (
                            :cardNo,
                            :name,
                            :gender,
                            :birthDate,
                            :phone,
                            :idNumber,
                            :address,
                            :emergencyContactName,
                            :emergencyContactPhone,
                            datetime('now'),
                            datetime('now')
                        );
                        '''

            # 将 CreatePatient 对象的字段传递给 SQL
            cursor.execute(sql, {
                'cardNo': patient.cardNo,
                'name': patient.name,
                'gender': patient.gender,
                'birthDate': patient.birthDate,
                'phone': patient.phone,
                'idNumber': patient.idNumber,
                'address': patient.address,
                'emergencyContactName': patient.emergencyContactName,
                'emergencyContactPhone': patient.emergencyContactPhone
            })

            # 提交更改
            con.commit()

    def updatePatient(self, patient: UpdatePatient):
        # 连接数据库
        with sqlite3.connect(self.dbFile) as con:
            cursor = con.cursor()

            # 修改患者信息的 SQL 语句
            sql = '''
                    UPDATE patients
                    SET
                        cardNo = :cardNo,
                        name = :name,
                        gender = :gender,
                        birthDate = :birthDate,
                        phone = :phone,
                        idNumber = :idNumber,
                        address = :address,
                        emergencyContactName = :emergencyContactName,
                        emergencyContactPhone = :emergencyContactPhone,
                        updatedTime = datetime('now')
                    WHERE userId = :userId;
                    '''

            # 将 UpdatePatient 对象的字段传递给 SQL
            cursor.execute(sql, {
                'userId': patient.userId,
                'cardNo': patient.cardNo,
                'name': patient.name,
                'gender': patient.gender,
                'birthDate': patient.birthDate,
                'phone': patient.phone,
                'idNumber': patient.idNumber,
                'address': patient.address,
                'emergencyContactName': patient.emergencyContactName,
                'emergencyContactPhone': patient.emergencyContactPhone
            })

            # 提交更改
            con.commit()




