
from sqlalchemy.orm import sessionmaker
from DBManager.TableClasses.Users import *
from DBManager.TableClasses.Favorites import *


class AddUserFavoritesClass():

    def __init__(self):
        self._session = sessionmaker()()

    def AddUserFavorites(self, user_id : int, fav_id : int) -> bool:
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
