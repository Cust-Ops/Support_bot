from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

bitrix_b = KeyboardButton('Создание запроса')
office_b = KeyboardButton('Статус запроса')
requests_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
requests_kb.add(bitrix_b, office_b)

inline_yn_doc_1 = InlineKeyboardButton('Да', callback_data='btn_y')
inline_yn_doc_2 = InlineKeyboardButton('Нет', callback_data='btn_n')
inline_yn_full = InlineKeyboardMarkup(row_width=2).add(inline_yn_doc_1, inline_yn_doc_2)

