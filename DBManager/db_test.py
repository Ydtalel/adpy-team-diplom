from random import randrange
from DBManager.DBManager import DBManager


def DbTest():

    db = DBManager(db_name="vkbot_db", user_name="postgres", user_password="111")

    x = db.AddUser(vk_id="eezz" + str(randrange(100)), name="vasya", age=23, gender=1, city=1)
    print("AddUser", x)

    x = db.GetUserByID(1)
    print("GetUserByID", x)
    x = db.GetUserByVkID("eezz11")
    print("GetUserByVkID", x)

    x = db.AddUserFavorites(1, 3)
    print("AddUserFavorites", x)
    x = db.AddUserFavorites(1, 4)
    print("AddUserFavorites", x)

    x = db.GetUserFavoritesVkIDList("eezz23")
    print("GetUserFavorites", x)

    x = db.AddViewPastVkID(1, "Pstvk_id1")
    print("AddViewPastVkID", x)

    x = db.GetViewPastVkIDList(1)
    print(x)
