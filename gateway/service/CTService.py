from typing import List

from Exception.DataBaseException import DataBaseException
from gateway.dao.CTDaoInterface import CTDaoInterface
from gateway.dao.CTDaoOrm import CTDaoOrm
from pojo.CT import CT

class CTService:
    def __init__(self):
        self.CTDao : CTDaoInterface = CTDaoOrm()

    def getAllCT(self) -> List[CT]:
        try:
            return self.CTDao.getAllCT()
        except Exception as e:
            raise DataBaseException(e.args[0])



