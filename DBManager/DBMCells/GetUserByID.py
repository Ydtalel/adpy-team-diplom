
from sqlalchemy.orm import sessionmaker
from DBManager.TableClasses.Users import *
from DBManager.TableClasses.Favorites import *


class GetUserByIDClass():

    def __init__(self, session):
        self._session = session

    def GetUserByID(self, user_id : int) -> dict:
        """Get user by user_id in database\n
        Return Dictionary, not empty if successfull."""
        x_ret = self._session.query(User).where(User.user_id == user_id)
        for x in x_ret.all():
            return {"name" : x.name, "age" : x.age, "gender" : x.gender, "city" : x.city, "vk_id" : x.user_vk_id, "user_id" : user_id}
        return {}
