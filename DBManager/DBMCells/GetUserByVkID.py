
from sqlalchemy.orm import sessionmaker
from DBManager.TableClasses.Users import *
from DBManager.TableClasses.Favorites import *


class GetUserByVkIDClass():

    def __init__(self):
        self._session = sessionmaker()()

    def GetUserByVkID(self, vk_id : str) -> dict:
        """Get user by VK_ID in database\n
        Return Dictionary, not empty if successfull."""
        x_ret = self._session.query(User).where(User.user_vk_id == vk_id)
        for x in x_ret.all():
            return {"name" : x.name, "age" : x.age, "gender" : x.gender, "city" : x.city, "vk_id" : x.user_vk_id, "user_id" : x.user_id}
        return {}
