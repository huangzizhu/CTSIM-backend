from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import  relationship
from gateway.orm.OrmEngine import OrmEngine


class VisitOrm(OrmEngine().getBase()):
    __tablename__ = "visits"

    visitId = Column(Integer, primary_key=True, autoincrement=True)
    patientId = Column(Integer, ForeignKey("patients.pid"), nullable=False)
    doctorId = Column(Integer, ForeignKey("user.uid"), nullable=False)

    visitTime = Column(String, nullable=False)         # YYYY-MM-DD HH:MM:SS
    isEmergency = Column(Integer, nullable=False, default=0)
    symptoms = Column(Text, nullable=False)

    department = Column(String, nullable=True)
    diagnosis = Column(Text, nullable=True)
    triageLevel = Column(Integer, nullable=True)
    status = Column(String, nullable=False, default="ongoing")

    createdTime = Column(String, nullable=False, server_default=func.datetime('now'))
    updatedTime = Column(String, nullable=True)

    # 可选：添加关系，方便 ORM 查询关联对象
    patient = relationship("PatientOrm", back_populates="visits", foreign_keys=[patientId])
    doctor = relationship("UserOrm", back_populates="visits", foreign_keys=[doctorId])
    ct_orders = relationship("CTOrderOrm", back_populates="visit")