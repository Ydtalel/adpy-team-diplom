
import sqlalchemy as sa
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from DBManager.DeclarativeBase import DeclarativeBase

class SessionMakerClass():

    def __init__(self, db_name : str, user_name : str, user_password : str, db_protocol : str = "postgresql", host : str = "localhost", port : str = "5432"):
        self.__DSN = F"{db_protocol}://{user_name}:{user_password}@{host}:{port}/{db_name}"
        self.__engine = sa.create_engine(self.__DSN)
        DeclarativeBase.Base.metadata.create_all(self.__engine)
        self._session = sessionmaker(bind=self.__engine)()

    def GetSession(self):
        return self._session
