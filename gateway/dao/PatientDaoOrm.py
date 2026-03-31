from gateway.dao.PatientDaoInterface import PatientDaoInterface
from gateway.orm.OrmEngine import OrmEngine
from gateway.orm.PatientOrm import PatientOrm
from pojo.Patient import CreatePatient, UpdatePatient, Patient
from sqlalchemy import update, func

class PatientDaoOrm(PatientDaoInterface):
    def __init__(self):
        super().__init__('patientDaoOrm')
        self.engine = OrmEngine()
        # 保存 Session 工厂
        self.SessionLocal = self.engine.createSessionFactory()

    def addPatient(self, patient: CreatePatient):
        session = self.SessionLocal()
        patientOrm = PatientOrm(**patient.__dict__)
        try:
            session.add(patientOrm)
            session.commit()
            return Patient.from_orm()
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
            return [    Patient(
                        **{
                            **patient.__dict__,
                            "createdTime": patient.createdTime.isoformat(),
                            "updatedTime": patient.updatedTime.isoformat()
                        })
                        for patient in patients]

        finally:
            session.close()

    def getPatientById(self, pid: int) -> Patient | None:
        session = self.SessionLocal()
        try:
            orm: PatientOrm = session.query(PatientOrm).filter(PatientOrm.pid == pid).one_or_none()
            if not orm:
                return None
            return Patient(
                **{
                    **orm.__dict__,
                    "createdTime": orm.createdTime.isoformat(),
                    "updatedTime": orm.updatedTime.isoformat()
                }
            )
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

