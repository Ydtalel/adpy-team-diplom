import vk
from dotenv import load_dotenv
import os
import random
from datetime import date
from DBManager.DBManager import DBManager

# import time
# from Bot_Valera.conf import token_1

# token = token_1

db_manager = DBManager(db_name='vkinder', db_protocol="postgresql", user_name="postgres", user_password="yu14r06iy90",
                       host="localhost", port="5432")

## это не удаляем
load_dotenv()  # take environment variables from .env.
token = os.getenv('token')
bot_token = os.getenv('bot_token')
bd_password = os.getenv('bd_password ')


class Vkinder:

    def __init__(self, api):
        self.about_user_dict = {}
        self.api = api
        self.candidate_list = ['452461439']

    def get_user_info(self, id_, flag=False):
        user_info = self.api.users.get(user_ids=id_, fields='id, first_name, last_name, bdate, city, sex')
        try:
            age = int(date.today().year) - int(user_info[0]['bdate'].split('.')[2])
        except IndexError:
            age = 25
        sex = user_info[0]['sex']
        try:
            city_id = user_info[0]['city']['id']
        except KeyError:
            city_id = 1

        self.about_user_dict = {
            'vk_id': id_,
            'name': f"{user_info[0]['first_name']} {user_info[0]['last_name']}",
            'age': age,
            'sex': sex,
            'city': city_id,
            'photo_links': self._get_top3_photo(id_)
        }
        if flag:
            if sex == 1:
                sex = 2
            else:
                sex = 1

            users_search = self.api.users.search(count=50, is_closed=0, sort=0, has_photo=1, status=6, sex=sex,
                                                 age_from=age - 3, age_to=age + 3)
            self.candidate_list = [user['id'] for user in users_search['items'] if not user['is_closed']]
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
            dict_[str(photo['id'])] = largest['url']
        sorted_tuples = sorted(dict_.items(), key=lambda item: item[1])[-3:]
        return [id_ for id_ in {k: v for k, v in sorted_tuples}.keys()]

    def users_search(self):
        print(f' лист кандидатов - {self.candidate_list} , {type(self.candidate_list[0])}')
        next_user = random.choice(self.candidate_list)
        chat_user_id = db_manager.GetUserByVkID(str(self.about_user_dict['vk_id']))['user_id']  # 2
        print(f'chat_user_id  = {chat_user_id}')
        vk_id_list = db_manager.GetViewPastVkIDList(chat_user_id)
        print(f'vk_id_list  - {vk_id_list}, {type(vk_id_list[0])}')
        for candidate in self.candidate_list:
            print(f'candidate - {candidate}, {type(candidate)}')
            if str(candidate) not in vk_id_list:
                next_user = int(candidate)
                break
            else:
                print(f'ТУТ ПОВТОР кандидата {candidate}')
                del self.candidate_list[self.candidate_list.index(candidate)]
        print(f'next user - {next_user}, {type(next_user)}\n\n')

        del self.candidate_list[self.candidate_list.index(next_user)]
        user_info = self.api.users.get(user_ids=next_user, fields='id, first_name, last_name')
        photo_id = self._get_top3_photo(next_user)
        return {
            'name': f"{user_info[0]['first_name']} {user_info[0]['last_name']}",
            'link': f"https://vk.com/id{str(next_user)}",
            'photo': photo_id,
            'vk_id': next_user
        }

    def get_favorites(self, favorits_vk_id):
        favorites = self.api.users.get(user_ids=f'{",".join(favorits_vk_id)}', fields='first_name, last_name, id')
        fav_list = {}
        for fav in favorites:
            id_ = fav['id']
            fav_list[f"https://vk.com/id{id_}"] = f"{fav['first_name']} {fav['last_name']}"
        return fav_list

