# file: gateway/orm/CTOrm.py

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from gateway.orm.OrmEngine import OrmEngine


class CTOrm(OrmEngine().getBase()):
    __tablename__ = 'ct'

    ctId = Column(Integer, primary_key=True, autoincrement=True)
    deviceCode = Column(String(50), nullable=False, unique=True)
    deviceName = Column(String(100), nullable=False)
    model = Column(String(100), nullable=True)
    manufacturer = Column(String(100), nullable=True)
    category = Column(String(50), nullable=True)
    status = Column(String(20), nullable=False, default='正常')
    location = Column(String(100), nullable=False)
    notes = Column(String, nullable=True)

    createdAt = Column(
        DateTime,
        nullable=False,
        server_default=func.datetime('now', 'localtime')
    )
    updatedAt = Column(
        DateTime,
        nullable=False,
        server_default=func.datetime('now', 'localtime'),
        onupdate=func.datetime('now', 'localtime')
    )
    ct_orders = relationship("CTOrderOrm", back_populates="ct")