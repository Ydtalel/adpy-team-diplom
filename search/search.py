import vk
from dotenv import load_dotenv
import os
import random
from Bot_Valera.conf import token

token = token



## это не удаляем
# load_dotenv()  # take environment variables from .env.
# token = os.getenv('token')


class Vkinder:
    def __init__(self, api):
        self.api = api

    def get_user_info(self, id_):
        user_info = self.api.users.get(user_ids=id_, fields='id, first_name, last_name, bdate, city, sex')
        age = 2023 - int(user_info[0]['bdate'].split('.')[2])  # тут потом доделать что бы считал через date
        sex = user_info[0]['sex']
        city_id = user_info[0]['city']['id']
        fname = user_info[0]['first_name']
        lname = user_info[0]['last_name']
        return {
            'vk_id': id_,
            'name': f"{fname} {lname}",
            'age': age,
            'sex': sex,
            'city': city_id
        }

    def users_search(self, params):
        # sort -0 популярность //  sort-1 новые // count максимум 1000
        if params['sex'] == 1:
            params['sex'] = 2
        else:
            params['sex'] = 1
        del params['vk_id']
        del params['name']
        users_age = params.pop('age')
        params['age_from'] = users_age - 3
        params['age_to'] = users_age + 3

        users_search = self.api.users.search(**params, count=1000, is_closed=0, sort=0, has_photo=1, status=6)
        return [user['id'] for user in users_search['items'] if not user['is_closed']]

    @staticmethod
    def _find_largest_photo(dict_sizes):
        if dict_sizes["width"] >= dict_sizes["height"]:
            return dict_sizes["width"]
        else:
            return dict_sizes["height"]

    def _get_all_user_photo(self, id_):
        all_photos = self.api.photos.getAll(owner_id=id_, extended=True)
        dict_ = {}
        for photo in all_photos['items']:
            sizes = photo['sizes']
            largest = max(sizes, key=self._find_largest_photo)
            dict_[largest['url']] = str(photo['likes']['count'])
        sorted_tuples = sorted(dict_.items(), key=lambda item: item[1])[-3:]
        return {k: v for k, v in sorted_tuples}.keys()

    def get_candidate(self, list_of_users_id):
        rand_user = random.choice(list_of_users_id)
        user_info = self.api.users.get(user_ids=rand_user, fields='id, first_name, last_name')
        hrefs = self._get_all_user_photo(rand_user)
        return {
            'name': f"{user_info[0]['first_name']} {user_info[0]['last_name']}",
            'link': f"https://vk.com/id{str(user_info[0]['id'])}",
            'photo': hrefs
        }


vkinder = Vkinder(vk.API(access_token=token, v=5.131))

group_member = vkinder.get_user_info(922473)
candidate_list = vkinder.users_search(group_member)
print(vkinder.get_candidate(candidate_list))
