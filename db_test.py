<<<<<<< HEAD
from random import randrange
=======
>>>>>>> ae9c5b8433a47dd17d85838c5f6c5ec1a5509a7c
from DBManager.DBManager import DBManager

if __name__ == "__main__":
    db = DBManager("vkbot_db")
<<<<<<< HEAD
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
