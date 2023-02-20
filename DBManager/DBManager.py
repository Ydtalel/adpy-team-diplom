import sqlalchemy as sa
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from DBManager.DeclarativeBase import DeclarativeBase
from DBManager.TableClasses.Users import User
from DBManager.TableClasses.Favorites import Favorite


class DBManager:

    def __init__(self, db_name :str, db_protocol : str = "postgresql", user_name : str = "postgres", user_password : str = "wifi1993+", host : str = "localhost", port : str = "5432") -> None:
        self.__DSN = F"{db_protocol}://{user_name}:{user_password}@{host}:{port}/{db_name}"
        self.__engine = sa.create_engine(self.__DSN)
        DeclarativeBase.Base.metadata.create_all(self.__engine)
        self.__session = sessionmaker(bind=self.__engine)()

    def AddUser(self, vk_id: str, name: str, age: int, gender: int):
        self.__session.add(User(user_vk_id=vk_id, name=name, age=age, gender=gender))
        self.__session.commit()

    def AddUserFavorites(self, user_id : int, fav_id : int):
        self.__session.add(Favorite(user_id=user_id, user_fav_id=fav_id))
        self.__session.commit()

    def GetUserByID(self, user_id : int) -> dict:
        x_ret = self.__session.query(User).where(User.user_id == user_id)
        for x in x_ret.all():
            return {"name" : x.name, "age" : x.age, "gender" : x.gender}
        return {}

    def GetUserByVkID(self, vk_id: str) -> dict:
        x_ret = self.__session.query(User).where(User.user_vk_id == vk_id)
        for x in x_ret.all():
            return {"user_id" : x.user_id, "name" : x.name, "age" : x.age, "gender" : x.gender}
        return {}
    
    def GetUserFavorites(self, user_id : int) -> list:
        x_ret = self.__session.query(Favorite).where(Favorite.user_id == user_id)
        ret_list = list()
        for x in x_ret.all():
            ret_list.append(x.user_fav_id)
        return ret_list
