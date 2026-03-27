
from gateway.dao.PatientDaoInterface import PatientDaoInterface
from pojo.Patient import CreatePatient, UpdatePatient, Patient
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

    def updatePatient(self, patient: UpdatePatient) -> int:
        # 连接数据库
        with sqlite3.connect(self.dbFile) as con:
            cursor = con.cursor()

            # 需要动态生成的 SQL 语句开始部分
            sql = 'UPDATE patients SET '

            # 动态设置字段和值的部分
            fields = {}
            update_fields = []

            # 只添加非 None 的字段
            if patient.cardNo is not None:
                update_fields.append("cardNo = :cardNo")
                fields['cardNo'] = patient.cardNo
            if patient.name is not None:
                update_fields.append("name = :name")
                fields['name'] = patient.name
            if patient.gender is not None:
                update_fields.append("gender = :gender")
                fields['gender'] = patient.gender
            if patient.birthDate is not None:
                update_fields.append("birthDate = :birthDate")
                fields['birthDate'] = patient.birthDate
            if patient.phone is not None:
                update_fields.append("phone = :phone")
                fields['phone'] = patient.phone
            if patient.idNumber is not None:
                update_fields.append("idNumber = :idNumber")
                fields['idNumber'] = patient.idNumber
            if patient.address is not None:
                update_fields.append("address = :address")
                fields['address'] = patient.address
            if patient.emergencyContactName is not None:
                update_fields.append("emergencyContactName = :emergencyContactName")
                fields['emergencyContactName'] = patient.emergencyContactName
            if patient.emergencyContactPhone is not None:
                update_fields.append("emergencyContactPhone = :emergencyContactPhone")
                fields['emergencyContactPhone'] = patient.emergencyContactPhone

            # 加入更新时间
            update_fields.append("updatedTime = datetime('now')")

            # 合并字段部分
            sql += ', '.join(update_fields)

            # 加上 WHERE 子句
            sql += ' WHERE pid = :pid'

            # 把 pid 加入到字段字典中
            fields['pid'] = patient.pid

            # 执行 SQL
            cursor.execute(sql, fields)

            return cursor.rowcount  # 返回受影响的行数

    def getAllPatients(self):
        with sqlite3.connect(self.dbFile) as con:
            cursor = con.cursor()
            sql = 'SELECT * FROM patients'
            cursor.execute(sql)
            rows = cursor.fetchall()
            patients = []
            for row in rows:
                patients.append(Patient(
                    pid=row[0],
                    cardNo=row[1],
                    name=row[2],
                    gender=row[3],
                    birthDate=row[4],
                    phone=row[5],
                    idNumber=row[6],
                    address=row[7],
                    emergencyContactName=row[8],
                    emergencyContactPhone=row[9],
                    createdTime=row[10],
                    updatedTime=row[11]
                    )
                )
            return patients

    def deletePatient(self, pid) -> int:
        with sqlite3.connect(self.dbFile) as con:
            cursor = con.cursor()
            sql = 'DELETE FROM patients WHERE pid = :pid'
            cursor.execute(sql, {'pid': pid})
            con.commit()
            return cursor.rowcount

