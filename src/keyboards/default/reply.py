from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

start_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Каталог'), KeyboardButton(text='Корзина')],
    [KeyboardButton(text='Личный кабинет'), KeyboardButton(text='Вопросы и ответы')],
], resize_keyboard=True, input_field_placeholder='Выберете необходимую опцию')

account_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Настройки')],
    [KeyboardButton(text='История заказов')],
    [KeyboardButton(text='Главное меню')],
], resize_keyboard=True, input_field_placeholder='Выберете необходимую опцию')

back_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Назад')],
], resize_keyboard=True, one_time_keyboard=True)

settings_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Имя'), KeyboardButton(text='Номер')],
                                            [KeyboardButton(text='Главное меню')]],
                                  resize_keyboard=True, one_time_keyboard=True)

send_contact_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Отправить свой контакт', request_contact=True)]
], resize_keyboard=True, one_time_keyboard=True)

faq_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Общие вопросы')],
                                       [KeyboardButton(text='Наши контакты')],
                                       [KeyboardButton(text='Главное меню')],
                                       ], resize_keyboard=True, one_time_keyboard=True)

questions_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Как сделать заказ?')],
                                             [KeyboardButton(text='Какие бренды поставляет наша компания?')],
                                             [KeyboardButton(text='Главное меню')]
                                             ], resize_keyboard=True, one_time_keyboard=True)
