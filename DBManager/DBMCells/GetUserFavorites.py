
from sqlalchemy.orm import sessionmaker
from DBManager.TableClasses.Users import *
from DBManager.TableClasses.Favorites import *


class GetUserFavoritesClass():

    def __init__(self):
        self._session = sessionmaker()()

    def GetUserFavorites(self, user_id : int) -> list:
        """Get user favorites users id's LIST by user_id in database\n
        Return LIST, not empty if successfull."""
        x_ret = self._session.query(Favorite).where(Favorite.user_id == user_id)
        ret_list = list()
        for x in x_ret.all():
            ret_list.append(x.user_fav_id)
        return ret_list
