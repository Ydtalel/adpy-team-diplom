from sqlalchemy.orm import sessionmaker
from DBManager.TableClasses.Users import *
from DBManager.TableClasses.Favorites import *
from DBManager.TableClasses.UsersViewsPast import *

class AddViewPastVkIDClass():

    def __init__(self, session):
        self._session = session

    def AddViewPastVkID(self, user_id : int, past_vk_id : str) -> bool:
        """Add past viewed user to black list by VK_ID\n
        Return True if successfull."""
        if len(self._session.query(User).where(User.user_id == user_id).all()) < 1:
            return False
        if len(self._session.query(UsersViewPast).where(UsersViewPast.user_viewpast_vkid == past_vk_id).all()) > 0:
            return False
        self._session.add(UsersViewPast(user_id=user_id, user_viewpast_vkid=past_vk_id))
        self._session.commit()
        return True

