import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from conf import access_token, token_1
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from DBManager.DBManager import DBManager
from search.search import Vkinder
import vk


vk_session = vk_api.VkApi(token=access_token)
session_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)
dbmanager = DBManager("vkbot_db")
vkinder = Vkinder(vk.API(access_token=token_1, v=5.131))

def send_some_ms(vk_user_id, message_text, keyboard):
    vk_session.method('messages.send', {'user_id': vk_user_id,
                                        'message': message_text,
                                        'random_id': 0,
                                        'keyboard': keyboard.get_keyboard()})




def bot_valera():
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            msg = event.text.lower()
            vk_user_id = event.user_id
            keyboard = VkKeyboard()
            keyboard_start = VkKeyboard(one_time=True)
            keyboard_start.add_button('start', VkKeyboardColor.PRIMARY)
            #keyboard.add_line()
            keyboard.add_button('next', VkKeyboardColor.POSITIVE)
            keyboard.add_line()
            keyboard.add_button('добавить в избранное', VkKeyboardColor.PRIMARY)
            keyboard.add_button('список избранного', VkKeyboardColor.PRIMARY)

            if msg == 'start':
                user_info = vkinder.get_user_info(vk_user_id)
                dbmanager.AddUser(str(vk_user_id),
                                  user_info['name'],
                                  30,
                                  user_info['sex'],
                                  user_info['city']
                                  )
                send_some_ms(vk_user_id,
                             'Привет! Я бот Валера, и я готов помочь вам найти свою вторую половинку. Жми next и начнем!',
                             keyboard)
            elif msg == 'next':
                # отпровляем пользователю подходящую пару
                couple_url = vkinder.users_search()
                sr = f'{couple_url["name"]}\n' \
                     f'{couple_url["link"]}\n' \
                     f'{couple_url["photo"]}'
                send_some_ms(vk_user_id, sr, keyboard)
            elif msg == 'добавить в избранное':
                # тут используем метод класса бд
                candidate_vk_id = couple_url["vk_id"]
                candidate_info = vkinder.get_user_info(candidate_vk_id)
                dbmanager.AddUser(str(candidate_vk_id),
                                  candidate_info['name'],
                                  30,
                                  candidate_info['sex'],
                                  candidate_info['city'])
                candidate_db = dbmanager.GetUserByVkID(candidate_vk_id)
                x = candidate_db['user_id']
                get_user = dbmanager.GetUserByVkID(str(vk_user_id))
                dbmanager.AddUserFavorites(get_user["user_id"], x)
                send_some_ms(vk_user_id, 'jr', keyboard)
            elif msg == 'список избранного':
                # тут используем метод бд с запросом к бд
                get_user = dbmanager.GetUserByVkID(str(vk_user_id))
                y = dbmanager.GetUserFavorites(get_user["user_id"])
                for i in y:
                    send_some_ms(vk_user_id, i, keyboard)
            else:
                send_some_ms(vk_user_id, 'Нажми старт что бы начать', keyboard_start)



bot_valera()
