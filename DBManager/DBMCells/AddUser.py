
from sqlalchemy.orm import sessionmaker
from DBManager.TableClasses.Users import *


class AddUserClass():

    def __init__(self):
        self._session = sessionmaker()() # beauty requires sacrifice

    def AddUser(self, vk_id: str, name: str, age: int, gender: int, city : int) -> bool:
        """Adding user to database. All parameters are obligatory\n
        Parameters:\n
        Vk_id is a short string\n
        Name is a string\n
        Age parameter is integer > 0\n
        Gender is Male = 1, Female = 0\n
        City is INTEGER\n
        Return True if added successfull otherwise false.\n"""  
        if age < 1: return False
        x_ret = self._session.query(User).where(User.user_vk_id == vk_id)
        if len(x_ret.all()) > 0:
            return False
        self._session.add(User(user_vk_id=vk_id, name=name, age=age, gender=gender, city=city))
        self._session.commit()
        return True
