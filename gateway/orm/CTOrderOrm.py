from sqlalchemy import Column, Integer, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship
from gateway.orm.OrmEngine import OrmEngine
from datetime import datetime


# 状态常量
class StatusEnum:
    PENDING = 0     # 待排队
    QUEUING = 1     # 排队中
    SCANNING = 2    # 扫描中
    COMPLETED = 3   # 已完成
    CANCELED = 4    # 已取消
    EXPIRED = 5     # 过期

# 优先级常量
class PriorityEnum:
    NORMAL = 0      # 普通
    EMERGENCY = 1   # 急诊
    VIP = 2         # VIP

class CTOrderOrm(OrmEngine().getBase()):
    __tablename__ = 'ct_order'

    orderId = Column(Integer, primary_key=True, autoincrement=True)
    patientId = Column(Integer, ForeignKey('patient.patientId'), nullable=False)
    visitId = Column(Integer, ForeignKey('visit.visitId'), nullable=False)
    ctId = Column(Integer, ForeignKey('ct.ctId'), nullable=False)

    status = Column(Integer, nullable=False)       # 0-5 对应 StatusEnum
    scheduledTime = Column(DateTime, nullable=False)
    queueEnterTime = Column(DateTime)
    startTime = Column(DateTime)
    endTime = Column(DateTime)
    expectedDuration = Column(Integer)             # 预计扫描时长（分钟）
    actualDuration = Column(Integer)               # 实际扫描时长（分钟）
    priority = Column(Integer, default=PriorityEnum.NORMAL)  # 0-2 对应 PriorityEnum
    isEmergency = Column(Boolean, default=False)
    notes = Column(Text)
    createdAt = Column(DateTime, default=datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    canceledAt = Column(DateTime)

    # relationships
    patient = relationship("PatientOrm", back_populates="ct_orders",foreign_keys=[patientId])
    visit = relationship("VisitOrm", back_populates="ct_orders",foreign_keys=[visitId])
    ct = relationship("CTOrm", back_populates="ct_orders",foreign_keys=[ctId])

    def __repr__(self):
        return f"<CTOrder(orderId={self.orderId}, status={self.status}, patientId={self.patientId})>"