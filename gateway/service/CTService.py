from typing import List

from Exception.DataBaseException import DataBaseException
from gateway.dao.CTDaoInterface import CTDaoInterface
from gateway.dao.CTDaoOrm import CTDaoOrm
from pojo.CT import CT
from pojo.CTOrder import CTOrderCreate,CTOrderUpdate,CTOrder


class CTService:
    def __init__(self):
        self.CTDao : CTDaoInterface = CTDaoOrm()

    def getAllCT(self) -> List[CT]:
        try:
            return self.CTDao.getAllCT()
        except Exception as e:
            raise DataBaseException(e.args[0])

    def addCTOrder(self, order: CTOrderCreate) -> CTOrder:
        try:
            return self.CTDao.addCTOrder(order)
        except Exception as e:
            raise DataBaseException(e.args[0])



