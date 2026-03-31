from sqlalchemy import Column, Integer, String, Enum, Index
from sqlalchemy.orm import  relationship

from gateway.orm.OrmEngine import OrmEngine


class UserOrm(OrmEngine().getBase()):
    __tablename__ = 'user'

    uid = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(20), nullable=False, unique=True)
    hashedPassword = Column(String, nullable=False)
    level = Column(Integer, nullable=False, default=0)
    visits = relationship("VisitOrm", back_populates="doctor")
