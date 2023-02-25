import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from Bot_Valera.configurations import token_group, access_token, Db_password
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from DBManager.DBManager import DBManager
from search.search import Vkinder
import vk


vk_session = vk_api.VkApi(token=token_group)
session_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)
dbmanager = DBManager("vkbot_db", 'postgres', Db_password)
vkinder = Vkinder(vk.API(access_token=access_token, v=5.131))


def send_some_ms(vk_user_id, message_text, keyboard, attachment=None):
    vk_session.method('messages.send', {'user_id': vk_user_id,
                                        'message': message_text,
                                        'random_id': 0,
                                        'keyboard': keyboard.get_keyboard(),
                                        'attachment': attachment
                                        })


def bot_valera():
    candidat_list = []
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            msg = event.text.lower()
            vk_user_id = event.user_id
            keyboard = VkKeyboard()
            keyboard_start = VkKeyboard(one_time=True)
            keyboard_start.add_button('start', VkKeyboardColor.PRIMARY)
            keyboard.add_button('next', VkKeyboardColor.POSITIVE)
            keyboard.add_line()
            keyboard.add_button('список избранного', VkKeyboardColor.PRIMARY)
            keyboard_2 = VkKeyboard()
            keyboard_2.add_button('next', VkKeyboardColor.POSITIVE)
            keyboard_2.add_line()
            keyboard_2.add_button('добавить в избранное', VkKeyboardColor.PRIMARY)
            keyboard_2.add_line()
            keyboard_2.add_button('список избранного', VkKeyboardColor.PRIMARY)
            if msg == 'start':
                user_info = vkinder.get_user_info(vk_user_id, flag=True)
                dbmanager.AddUser(str(vk_user_id),
                                  user_info['name'],
                                  user_info['age'],
                                  user_info['sex'],
                                  user_info['city']
                                  )
                send_some_ms(vk_user_id,
                             'Привет! Я бот Валера, и я готов помочь вам найти свою вторую половинку. '
                             'Жми next и начнем!',
                             keyboard)
            elif msg == 'next':
                vkinder.get_user_info(vk_user_id)
                couple_url = vkinder.users_search()
                chat_user_db_id = dbmanager.GetUserByVkID(str(vk_user_id))["user_id"]
                dbmanager.AddViewPastVkID(user_id=chat_user_db_id, past_vk_id=str(couple_url['vk_id']))
                info_fav = vkinder.get_user_info(couple_url['vk_id'])
                favorit_name_link = f'{couple_url["name"]}\n' \
                                    f'{couple_url["link"]}\n'
                send_some_ms(vk_user_id, favorit_name_link, keyboard_2)
                candidat_list.append(couple_url['vk_id'])
                for i in info_fav["photo_links"]:
                    attachment = f'photo{couple_url["vk_id"]}_{i}'
                    send_some_ms(vk_user_id, ' ', keyboard_2, attachment)
            elif msg == 'добавить в избранное':
                candidate_vk_id = couple_url['vk_id']
                candidate_info = vkinder.get_user_info(candidate_vk_id)
                dbmanager.AddUser(str(candidate_vk_id),
                                  candidate_info['name'],
                                  candidate_info['age'],
                                  candidate_info['sex'],
                                  candidate_info['city'])
                candidate_db = dbmanager.GetUserByVkID(str(candidate_vk_id))
                x = candidate_db['user_id']
                get_user = dbmanager.GetUserByVkID(str(vk_user_id))
                dbmanager.AddUserFavorites(get_user["user_id"], x)
                answer = f'{candidate_info["name"]} добавлен(а) в ваш список избранного.\n' \
                         f'Продолжим ? '
                send_some_ms(vk_user_id, answer, keyboard)
            elif msg == 'список избранного':
                y = dbmanager.GetUserFavoritesVkIDList(str(vk_user_id))
                for i in y:
                    f_u_vk_id = dbmanager.GetUserByVkID(str(i))
                    answe_2 = f'{f_u_vk_id["name"]}\nhttps://vk.com/id{f_u_vk_id["vk_id"]}'
                    send_some_ms(vk_user_id, answe_2, keyboard)
            else:
                send_some_ms(vk_user_id, 'Нажми старт что бы начать', keyboard_start)


# bot_valera()
