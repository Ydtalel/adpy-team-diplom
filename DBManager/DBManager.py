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
from DBManager.DBMCells.AddViewPastVkID import AddViewPastVkIDClass
from DBManager.DBMCells.GetViewPastVkID import GetViewPastVkIDClass


# TODO Complex requests to database

class DBManager():

    def __init__(self, db_name: str, user_name: str, user_password: str, db_protocol: str = "postgresql",
                 host: str = "localhost", port: str = "5432") -> None:
        self._session_obj = SessionMakerClass(db_name, user_name, user_password, db_protocol, host, port)
        self._session = self._session_obj.GetSession()

        self.AddUser = AddUserClass(self._session).AddUser
        self.AddUserFavorites = AddUserFavoritesClass(self._session).AddUserFavorites
        self.GetUserByID = GetUserByIDClass(self._session).GetUserByID
        self.GetUserByVkID = GetUserByVkIDClass(self._session).GetUserByVkID
        self.GetUserFavoritesVkIDList = GetUserFavoritesClass(self._session).GetUserFavoritesVkIDList
        self.AddViewPastVkID = AddViewPastVkIDClass(self._session).AddViewPastVkID
        self.GetViewPastVkIDList = GetViewPastVkIDClass(self._session).GetViewPastVkIDList
