
import sqlalchemy as sa
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

from DBManager.DeclarativeBase import DeclarativeBase
from DBManager.TableClasses.Users import User
from DBManager.TableClasses.Favorites import Favorite


class DBManager:

    def __init__(self, db_name :str, db_protocol : str = "postgresql", user_name : str = "postgres", user_password : str = "111", host : str = "localhost", port : str = "5432") -> None:
        self.__DSN = F"{db_protocol}://{user_name}:{user_password}@{host}:{port}/{db_name}"
        self.__engine = sa.create_engine(self.__DSN)
        DeclarativeBase.Base.metadata.create_all(self.__engine)
        self.__session = sessionmaker(bind=self.__engine)()

    def AddUser(self, vk_id: str, name: str, age: int, gender: int, city : int) -> bool:
        """Adding user to database. All parameters are obligatory\n
        Parameters:\n
        Vk_id is a short string\n
        Name is a string\n
        Age parameter is integer > 0\n
        Gender is Male = 1, Female = 0\n
        City is INTEGER\n
        Return True if added successfull otherwise false.\n"""
        if age < 1: return False
        x_ret = self.__session.query(User).where(User.user_vk_id == vk_id)
        if len(x_ret.all()) > 0:
            return False
        self.__session.add(User(user_vk_id=vk_id, name=name, age=age, gender=gender, city=city))
        self.__session.commit()
        return True

    def AddUserFavorites(self, user_id : int, fav_id : int) -> bool:
        """Adding favorited user to a user_id. All parameters are obligatory\n
        Parameters:\n
        user_id is user_id in database\n
        fav_id is favorited user in database\n
        Return True if added successfull otherwise false.\n"""
        if len(self.__session.query(User).where(User.user_id == user_id).all()) < 1:
            return False
        if len(self.__session.query(User).where(User.user_id == fav_id).all()) < 1:
            return False
        x_ret = self.__session.query(Favorite).where(Favorite.user_id == user_id)
        for x in x_ret.all():
            if x.user_fav_id == fav_id:
                return False
        self.__session.add(Favorite(user_id=user_id, user_fav_id=fav_id))
        self.__session.commit()
        return True

    def GetUserByID(self, user_id : int) -> dict:
        """Get user by user_id in database\n
        Return Dictionary, not empty if successfull."""
        x_ret = self.__session.query(User).where(User.user_id == user_id)
        for x in x_ret.all():
            return {"name" : x.name, "age" : x.age, "gender" : x.gender}
        return {}

    def GetUserByVkID(self, vk_id: str) -> dict:
        """Get user by VK_ID in database\n
        Return Dictionary, not empty if successfull."""
        x_ret = self.__session.query(User).where(User.user_vk_id == vk_id)
        for x in x_ret.all():
            return {"user_id" : x.user_id, "name" : x.name, "age" : x.age, "gender" : x.gender}
        return {}
    
    def GetUserFavorites(self, user_id : int) -> list:
        """Get user favorites users id's LIST by user_id in database\n
        Return LIST, not empty if successfull."""
        x_ret = self.__session.query(Favorite).where(Favorite.user_id == user_id)
        ret_list = list()
        for x in x_ret.all():
            ret_list.append(x.user_fav_id)
        return ret_list

