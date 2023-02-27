from random import randrange
from DBManager.DBManager import DBManager


def DbTest():

    db = DBManager(db_name="vkbot_db", user_name="postgres", user_password="111")


    x = db.add_user( { "vk_id" : "eezz" + str(randrange(100)), "name" : "vasya", "age" : "23", "gender" : 1, "city" : 1 } )
    print("AddUser", x)

    x = db.get_user_by_id(1)
    print("GetUserByID", x)
    x = db.get_user_by_vk_id("eezz11")
    print("GetUserByVkID", x)

    x = db.add_user_favorites(1, 3)
    print("AddUserFavorites", x)
    x = db.add_user_favorites(1, 4)
    print("AddUserFavorites", x)

    x = db.get_user_favorites_vk_id_list("eezz12")
    print("GetUserFavorites", x)

    x = db.add_view_past_vk_id(1, "Pstvk_id2")
    print("AddViewPastVkID", x)

    x = db.get_view_past_vk_id_list(1)
    print(x)
