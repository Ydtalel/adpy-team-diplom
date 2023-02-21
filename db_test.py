
from random import randrange
from DBManager.DBManager import DBManager


if __name__ == "__main__":

    db = DBManager("vkbot_db")
    x = db.GetUserByVkID("ee3")
    print(x)
    x = db.AddUser("eezz" + str(randrange(100)), "vasya", age=23, gender=1, city=1)
    print("AddUser", x)
    x = db.AddUserFavorites(1, 3)
    print("AddUserFavorites", x)
    x = db.GetUserByID(1)
    print("GetUserByID", x)
    x = db.GetUserByVkID("eezz11")
    print("GetUserByVkID", x)
    x = db.GetUserFavorites(1)
    print("GetUserFavorites", x)

# git test 229
