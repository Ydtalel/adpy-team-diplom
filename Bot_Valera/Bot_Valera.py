import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from conf import access_token
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from DBManager.DBManager import DBManager
from search.search import get_user_info, users_search, get_all_user_photo, find_largest_photo


vk_session = vk_api.VkApi(token=access_token)
session_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)
dbmanager = DBManager("vkbot_db")


def send_some_ms(user_id, message_text, keyboard):
    vk_session.method('messages.send', {'user_id': user_id,
                                        'message': message_text,
                                        'random_id': 0,
                                        'keyboard': keyboard.get_keyboard()})







def bot_valera():
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            msg = event.text.lower()
            user_id = event.user_id
            keyboard = VkKeyboard()
            keyboard.add_button('добавить в избранное', VkKeyboardColor.PRIMARY)
            keyboard.add_button('next', VkKeyboardColor.POSITIVE)
            keyboard.add_line()
            keyboard.add_button('список избранного', VkKeyboardColor.PRIMARY)
            if msg == 'next':
                # вызываем фун с инфой по пользователю
                user_info = get_user_info(user_id)
                # записываем его в бд
                dbmanager.AddUser(user_id, user_info['city'], user_info['age_to'], user_info['sex'])
                # отпровляем пользователю подходящую пару
                couple_url = f'https://vk.com/id{users_search()[1]}'
                send_some_ms(user_id, couple_url, keyboard)
            elif msg == 'добавить в избранное':
                # тут используем метод класса бд
                send_some_ms(user_id, 'метод класса бд', keyboard)
            elif msg == 'список избранного':
                # тут используем метод бд с запросом к бд
                send_some_ms(user_id, 'метод бд с запросом к бд', keyboard)
            else:
                send_some_ms(user_id, 'Я тебя не понимаю попробуй кнопки', keyboard)



bot_valera()