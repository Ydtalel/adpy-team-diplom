import vk
from dotenv import load_dotenv
import os
from pprint import pprint
import time

token = 'vk1.a.K25g9hQS_PWH_JRxa5GYQcvKNeStyV9SJFB8tQRstsB2N_NT7jWZMJtQUNQaS4elZGD_HmbzFB_-tFidloId9gFZg21XdV0Dn-L0a8gPAVhMih3HFiuoBKuZBo5JZk7ybkzezrV15ulLRjXnb70CT59miY5cpbYZiVlTpcXayNL1nxLWz1HGOz1JHAeSNKhq1UtEqarFqQVu0O0bZo1BgA'


load_dotenv()  # take environment variables from .env.
token_ = os.getenv('token')
api = vk.API(access_token=token, v=5.131)


def get_user_info(id_):
    user_info = api.users.get(user_ids=id_, fields='id, first_name, last_name, bdate, city, sex')
    age = 2023 - int(user_info[0]['bdate'].split('.')[2])  # тут потом доделать что бы считал через date
    sex = user_info[0]['sex']
    city_id = user_info[0]['city']['id']
    if sex == 1:
        opposite_sex = 2
    else:
        opposite_sex = 1
    params = {
        'age_from': age,
        'age_to': age + 5,
        'sex': opposite_sex,
        'city': city_id
    }
    return params


def users_search():
    # sort -0 популярность //  sort-1 новые count максимум 1000
    users_search = api.users.search(**params, count=5, is_closed=0, sort=0, has_photo=1, status=6)
    return [user['id'] for user in users_search['items'] if not user['is_closed']]


def find_largest_photo(dict_sizes):
    if dict_sizes["width"] >= dict_sizes["height"]:
        return dict_sizes["width"]
    else:
        return dict_sizes["height"]


def get_all_user_photo(id_):
    all_photos = api.photos.getAll(owner_id=id_, extended=True)
    dict_ = {}
    for photo in all_photos['items']:
        sizes = photo['sizes']
        largest = max(sizes, key=find_largest_photo)
        dict_[largest['url']] = str(photo['likes']['count'])
    sorted_tuples = sorted(dict_.items(), key=lambda item: item[1])[-3:]
    return {k: v for k, v in sorted_tuples}.keys()
#
#
# def get_data_opposite_sex(list_of_users_id):
#     for user in list_of_users_id:
#         user_info = api.users.get(user_ids=user, fields='id, first_name, last_name')
#         hrefs = get_all_user_photo(user)
#         print(f"{user_info[0]['first_name']} {user_info[0]['last_name']} ссылка на профиль"
#               f" https://vk.com/id{str(user_info[0]['id'])}\n{hrefs}")
#         time.sleep(4)


# # для парня находим дувушек из того же города примерного возраста со статусом в поиске, с открытым профилем и фото
params = get_user_info(922473)
# get_data_opposite_sex(users_search())





# database_getCities = api.database.getCities(country_id=1, need_all=1)
# pprint(database_getCities)

# database_getCountries = api.database.getCountries(code='RU')
# pprint(database_getCountries)
