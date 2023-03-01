from vk_api.keyboard import VkKeyboard, VkKeyboardColor

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