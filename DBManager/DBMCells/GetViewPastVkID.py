from sqlalchemy.orm import sessionmaker
from DBManager.TableClasses.Users import *
from DBManager.TableClasses.Favorites import *
from DBManager.TableClasses.UsersViewsPast import *

class GetViewPastVkIDClass():

    def __init__(self):
        self._session = sessionmaker()()

    def GetViewPastVkIDList(self, user_id : int) -> list:
        """Get PAST views of specified user_id NOT vk_id\n
        Return LIST, not empty if successfull."""
        ret_list = list()
        if len(self._session.query(User).where(User.user_id == user_id).all()) < 1:
            return ret_list
        x_ret = self._session.query(UsersViewPast).where(UsersViewPast.user_id == user_id)
        for x in x_ret.all():
            ret_list.append(x.user_viewpast_vkid)
        return ret_list
