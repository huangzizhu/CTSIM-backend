from sqlalchemy import Column, Integer, String, DateTime
import datetime
from sqlalchemy.orm import relationship

from gateway.orm.OrmEngine import OrmEngine


class PatientOrm(OrmEngine().getBase()):
    __tablename__ = 'patients'
    pid = Column(Integer, primary_key=True, autoincrement=True)  # 内部自增主键
    cardNo = Column(String(20), nullable=False, unique=True)      # 就诊卡号 / 病历号
    name = Column(String(50), nullable=False)                      # 姓名
    gender = Column(String(1), nullable=False)                     # 性别（M/F/O）
    birthDate = Column(String(10), nullable=False)                 # 出生日期：YYYY-MM-DD
    phone = Column(String(11))                                     # 联系方式
    idNumber = Column(String(18), unique=True)                     # 身份证号
    address = Column(String(255))                                  # 地址
    emergencyContactName = Column(String(50))                       # 紧急联系人姓名
    emergencyContactPhone = Column(String(11))                     # 紧急联系人电话
    createdTime = Column(DateTime, default=datetime.datetime.utcnow)  # 创建时间
    updatedTime = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)  # 更新时间
    visits = relationship("VisitOrm", back_populates="patient")
    ct_orders = relationship("CTOrderOrm", back_populates="patient")