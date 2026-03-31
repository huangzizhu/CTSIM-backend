from ProjectRoot import getProjectRootPath
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


class OrmEngine:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_inited'):
            projectRoot = getProjectRootPath()
            self.dbFile: Path = projectRoot.joinpath("ct.db")
            self.DATABASE_URL = f"sqlite:///{self.dbFile.resolve().as_posix()}"
            self.engine = create_engine(self.DATABASE_URL, echo=True)
            self.Base = declarative_base()
            self.Base.metadata.create_all(self.engine)
            self._inited = True


    def createSessionFactory(self):
       return sessionmaker(bind=self.engine)

    def getBase(self):
        return self.Base