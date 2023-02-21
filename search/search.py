import vk
# from dotenv import load_dotenv
# import os
import random
from datetime import date
# from Bot_Valera.conf import token_1
#
# token = token_1


## это не удаляем
# load_dotenv()  # take environment variables from .env.
# token = os.getenv('token')

class Vkinder:
    about_user_dict = {}

    def __init__(self, api):
        self.api = api

    def get_user_info(self, id_):
        user_info = self.api.users.get(user_ids=id_, fields='id, first_name, last_name, bdate, city, sex')
        #age = int(date.today().year) - int(user_info[0]['bdate'].split('.')[2])
        sex = user_info[0]['sex']
        city_id = user_info[0]['city']['id']
        fname = user_info[0]['first_name']
        lname = user_info[0]['last_name']
        Vkinder.about_user_dict = {
            'vk_id': id_,
            'name': f"{fname} {lname}",
            'age': 30,
            'sex': sex,
            'city': city_id
        }
        return self.about_user_dict

    @staticmethod
    def _find_largest_photo(dict_sizes):
        if dict_sizes["width"] >= dict_sizes["height"]:
            return dict_sizes["width"]
        else:
            return dict_sizes["height"]

    def _get_top3_photo(self, id_):
        all_photos = self.api.photos.getAll(owner_id=id_, extended=True)
        dict_ = {}
        for photo in all_photos['items']:
            sizes = photo['sizes']
            largest = max(sizes, key=self._find_largest_photo)
            dict_[largest['url']] = str(photo['likes']['count'])
        sorted_tuples = sorted(dict_.items(), key=lambda item: item[1])[-3:]
        return {k: v for k, v in sorted_tuples}.keys()

    def users_search(self):
        params = self.about_user_dict.copy()
        if params['sex'] == 1:
            params['sex'] = 2
        else:
            params['sex'] = 1
        del params['vk_id']
        del params['name']
        users_age = params.pop('age')
        params['age_from'] = users_age - 3
        params['age_to'] = users_age + 3
        # sort -0 популярность //  sort-1 новые // count максимум 1000
        users_search = self.api.users.search(**params, count=1000, is_closed=0, sort=0, has_photo=1, status=6)
        id_list = [user['id'] for user in users_search['items'] if not user['is_closed']]
        rand_user = random.choice(id_list)
        user_info = self.api.users.get(user_ids=rand_user, fields='id, first_name, last_name')
        hrefs = self._get_top3_photo(rand_user)
        return {
            'name': f"{user_info[0]['first_name']} {user_info[0]['last_name']}",
            'link': f"https://vk.com/id{str(user_info[0]['id'])}",
            'photo': hrefs,
            'vk_id': (user_info[0]['id'])
        }


# vkinder = Vkinder(vk.API(access_token=token, v=5.131))
#
# print(vkinder.get_user_info(922473))
# print(vkinder.users_search())
