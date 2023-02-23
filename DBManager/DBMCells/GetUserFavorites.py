
from sqlalchemy.orm import sessionmaker
from DBManager.TableClasses.Users import *
from DBManager.TableClasses.Favorites import *


class GetUserFavoritesClass():

    def __init__(self):
        self._session = sessionmaker()()

    def GetUserFavoritesVkIDList(self, vk_id : str):
        """Get user favorites users id's LIST by user_id in database\n
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
