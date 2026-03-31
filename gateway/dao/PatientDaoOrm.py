from gateway.dao.PatientDaoInterface import PatientDaoInterface
from gateway.orm.OrmEngine import OrmEngine
from gateway.orm.PatientOrm import PatientOrm
from pojo.Patient import CreatePatient, UpdatePatient, Patient
from sqlalchemy import update, func

class PatientDaoOrm(PatientDaoInterface):

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_inited'):
            super().__init__('patientDaoOrm')
            self.engine = OrmEngine()
            # 保存 Session 工厂
            self.SessionLocal = self.engine.createSessionFactory()
            self._inited = True

    def addPatient(self, patient: CreatePatient) -> Patient:
        session = self.SessionLocal()
        patientOrm = PatientOrm(**patient.__dict__)
        try:
            session.add(patientOrm)
            session.commit()
            return Patient.model_validate(patientOrm)
        finally:
            session.close()

    def updatePatient(self, patient: UpdatePatient) -> int:
        session = self.SessionLocal()
        data = patient.dict(exclude_unset=True, exclude_none=True)
        data["updatedTime"] = func.now()
        data.pop("pid")
        try:
            result = session.execute(
                update(PatientOrm)
                .where(PatientOrm.pid == patient.pid)
                .values(**data)
            )
            session.commit()
            return result.rowcount
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def getAllPatients(self):
        session = self.SessionLocal()
        try:
            patients = session.query(PatientOrm).all()
            return [Patient.model_validate(patient) for patient in patients]

        finally:
            session.close()

    def getPatientById(self, pid: int) -> Patient | None:
        session = self.SessionLocal()
        try:
            orm: PatientOrm = session.query(PatientOrm).filter(PatientOrm.pid == pid).one_or_none()
            if not orm:
                return None
            return Patient.model_validate(orm)
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()


    def deletePatient(self, pid) -> int:
        session = self.SessionLocal()
        try:
            result = session.query(PatientOrm).filter(PatientOrm.pid == pid).delete()
            session.commit()
            return result
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

