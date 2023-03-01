import sqlalchemy as sa
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

from DBManager.DeclarativeBase import DeclarativeBase
from DBManager.TableClasses.Users import User
from DBManager.TableClasses.Favorites import Favorite
from DBManager.TableClasses.UsersViewsPast import UsersViewPast


class DBManager:

    def __init__(self, db_name: str, user_name: str, user_password: str, db_protocol: str = "postgresql", host: str = "localhost", port: str = "5432") -> None:
        self.__DSN = F"{db_protocol}://{user_name}:{user_password}@{host}:{port}/{db_name}"
        self.__engine = sa.create_engine(self.__DSN)
        DeclarativeBase.Base.metadata.create_all(self.__engine)
        self._session = sessionmaker(bind=self.__engine)()

    def add_user(self, user_info : dict) -> bool:
        """Adding user to database. All parameters are obligatory\n
        Parameters:\n
        Vk_id is a short string\n
        Name is a string\n
        Age parameter is integer > 0\n
        Gender is Male = 1, Female = 0\n
        City is INTEGER\n
        Return True if added successfull otherwise false.\n"""
        if not user_info['vk_id'] or not user_info['name'] or not int(user_info['age']) or not int(user_info['sex']) or not user_info['city']: return False
        if int(user_info['age']) < 1: return False
        x_ret = self._session.query(User).where(User.user_vk_id == user_info['vk_id'])
        if len(x_ret.all()) > 0: return False
        self._session.add(User(user_vk_id=user_info['vk_id'], name=user_info['name'], age=user_info['age'], gender=user_info['sex'], city=user_info['city']))
        self._session.commit()
        return True

    def add_user_favorites(self, user_id: int, fav_id: int) -> bool:
        """Adding favorited user to a user_id. All parameters are obligatory\n
        Parameters:\n
        user_id is user_id in database\n
        fav_id is favorited user in database\n
        Return True if added successfull otherwise false.\n"""
        if len(self._session.query(User).where(User.user_id == user_id).all()) < 1:
            return False
        if len(self._session.query(User).where(User.user_id == fav_id).all()) < 1:
            return False
        x_ret = self._session.query(Favorite).where(Favorite.user_id == user_id)
        for x in x_ret.all():
            if x.user_fav_id == fav_id:
                return False
        self._session.add(Favorite(user_id=user_id, user_fav_id=fav_id))
        self._session.commit()
        return True

    def add_view_past_vk_id(self, user_id: int, past_vk_id: str) -> bool:
        """Add past viewed user to black list by VK_ID\n
        Return True if successfull."""
        if len(self._session.query(User).where(User.user_id == user_id).all()) < 1:
            return False
        if len(self._session.query(UsersViewPast).where(UsersViewPast.user_viewpast_vkid == past_vk_id).all()) > 0:
            return False
        self._session.add(UsersViewPast(user_id=user_id, user_viewpast_vkid=past_vk_id))
        self._session.commit()
        return True

    def get_user_by_id(self, user_id: int) -> dict:
        """Get user by user_id in database\n
        Return Dictionary, not empty if successfull."""
        x_ret = self._session.query(User).where(User.user_id == user_id)
        for x in x_ret.all():
            return {"name": x.name, "age": x.age, "gender": x.gender, "city": x.city, "vk_id": x.user_vk_id,
                    "user_id": user_id}
        return {}

    def get_user_by_vk_id(self, vk_id: str) -> dict:
        """Get user by VK_ID in database\n
        Return Dictionary, not empty if successfull."""
        x_ret = self._session.query(User).where(User.user_vk_id == vk_id)
        for x in x_ret.all():
            return {"name": x.name, "age": x.age, "gender": x.gender, "city": x.city, "vk_id": x.user_vk_id,
                    "user_id": x.user_id}
        return {}

    def get_user_favorites_vk_id_list(self, vk_id: str):
        """Get user favorites users id's LIST by vk_id in database\n
        Return LIST, not empty if successfull."""
        ret_list = list()
        try:
            user_id = self._session.query(User).where(User.user_vk_id == vk_id).all()[0].user_id
        except:
            return ret_list
        favorite_ids = self._session.query(Favorite).where(Favorite.user_id == user_id)
        for x in favorite_ids.all():
            ret_list.append(self._session.query(User.user_vk_id).where(User.user_id == x.user_fav_id).all()[0][0])
        return ret_list

    def get_view_past_vk_id_list(self, user_id: int) -> list:
        """Get PAST views of specified user_id NOT vk_id\n
        Return LIST, not empty if successfull."""
        ret_list = list()
        if len(self._session.query(User).where(User.user_id == user_id).all()) < 1:
            return ret_list
        x_ret = self._session.query(UsersViewPast).where(UsersViewPast.user_id == user_id)
        for x in x_ret.all():
            ret_list.append(x.user_viewpast_vkid)
        return ret_list
