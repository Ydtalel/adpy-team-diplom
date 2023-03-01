import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from Bot_Valera.configurations import token_group, access_token, Db_password
from DBManager.DBManager import DBManager
from search.search import Vkinder
import vk
from keyboard.keyboard import keyboard_start, keyboard_2, keyboard


vk_session = vk_api.VkApi(token=token_group)
session_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)
dbmanager = DBManager("vkbot_db", 'postgres', Db_password)
vkinder = Vkinder(vk.API(access_token=access_token, v=5.131))


def check():
    chat_user_id = dbmanager.get_user_by_vk_id(str(vkinder.about_user_dict['vk_id']))['user_id']
    vk_id_list = dbmanager.get_view_past_vk_id_list(chat_user_id)
    for candidate in vkinder.candidate_list:
        if str(candidate) not in vk_id_list:
            vkinder.next_user = int(candidate)
            break
        else:
            del vkinder.candidate_list[vkinder.candidate_list.index(candidate)]


def send_some_ms(vk_user_id, message_text, keyboardd, attachment=None):
    vk_session.method('messages.send', {'user_id': vk_user_id,
                                        'message': message_text,
                                        'random_id': 0,
                                        'keyboard': keyboardd.get_keyboard(),
                                        'attachment': attachment
                                        })


def bot_valera():
    candidat_list = []
    couple_url_list = []
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            msg = event.text.lower()
            vk_user_id = event.user_id
            if msg == 'start':
                user_info = vkinder.get_user_info(vk_user_id, flag=True)
                dbmanager.add_user(user_info)
                send_some_ms(vk_user_id,
                             'Привет! Я бот Валера, и я готов помочь вам найти свою вторую половинку. '
                             'Жми next и начнем!',
                             keyboard)
            elif msg == 'next':
                vkinder.get_user_info(vk_user_id)
                couple_url = vkinder.users_search()
                couple_url_list.append(couple_url['vk_id'])
                check()
                chat_user_db_id = dbmanager.get_user_by_vk_id(str(vk_user_id))["user_id"]
                dbmanager.add_view_past_vk_id(user_id=chat_user_db_id, past_vk_id=str(couple_url['vk_id']))
                info_fav = vkinder.get_user_info(couple_url['vk_id'])
                favorit_name_link = f'{couple_url["name"]}\n' \
                                    f'{couple_url["link"]}\n'
                send_some_ms(vk_user_id, favorit_name_link, keyboard_2)
                candidat_list.append(couple_url['vk_id'])
                info_fav_join = f',photo{couple_url["vk_id"]}_'.join(info_fav["photo_links"])
                attachment = f'photo{couple_url["vk_id"]}_{info_fav_join}'
                send_some_ms(vk_user_id, ' ', keyboard_2, attachment)
            elif msg == 'добавить в избранное':
                candidate_vk_id = couple_url_list.pop()
                candidate_info = vkinder.get_user_info(candidate_vk_id)
                dbmanager.add_user(candidate_info)
                candidate_db = dbmanager.get_user_by_vk_id(str(candidate_vk_id))
                x = candidate_db['user_id']
                get_user = dbmanager.get_user_by_vk_id(str(vk_user_id))
                dbmanager.add_user_favorites(get_user["user_id"], x)
                answer = f'{candidate_info["name"]} добавлен(а) в ваш список избранного.\n' \
                         f'Продолжим ? '
                send_some_ms(vk_user_id, answer, keyboard)
            elif msg == 'список избранного':
                y = dbmanager.get_user_favorites_vk_id_list(str(vk_user_id))
                for i in y:
                    f_u_vk_id = dbmanager.get_user_by_vk_id(str(i))
                    answe_2 = f'{f_u_vk_id["name"]}\nhttps://vk.com/id{f_u_vk_id["vk_id"]}'
                    send_some_ms(vk_user_id, answe_2, keyboard)
            else:
                send_some_ms(vk_user_id, 'Нажми старт что бы начать', keyboard_start)


# bot_valera()
