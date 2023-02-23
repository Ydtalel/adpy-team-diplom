
# import sqlalchemy as sa
# from sqlalchemy.orm import declarative_base, relationship, sessionmaker

# from DBManager.DeclarativeBase import DeclarativeBase
from DBManager.TableClasses.Users import User
from DBManager.TableClasses.Favorites import Favorite
from DBManager.TableClasses.UsersViewsPast import UsersViewPast

from DBManager.SessionMakerClass import SessionMakerClass
from DBManager.DBMCells.AddUser import AddUserClass
from DBManager.DBMCells.AddUserFavorites import AddUserFavoritesClass
from DBManager.DBMCells.GetUserByID import GetUserByIDClass
from DBManager.DBMCells.GetUserByVkID import GetUserByVkIDClass
from DBManager.DBMCells.GetUserFavorites import GetUserFavoritesClass


class DBManager():

    def __init__(self, db_name : str, user_name : str, user_password : str, db_protocol : str = "postgresql", host : str = "localhost", port : str = "5432") -> None:

        self._session_obj = SessionMakerClass(db_name, user_name, user_password, db_protocol, host, port)
        self._session = self._session_obj.GetSession()
    
    AddUser = AddUserClass.AddUser
    AddUserFavorites = AddUserFavoritesClass.AddUserFavorites
    GetUserByID = GetUserByIDClass.GetUserByID
    GetUserByVkID = GetUserByVkIDClass.GetUserByVkID
    GetUserFavoritesVkIDList = GetUserFavoritesClass.GetUserFavoritesVkIDList
    
