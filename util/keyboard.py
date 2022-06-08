from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def generate_keyboard():
    inline_kb_full = InlineKeyboardMarkup(row_width=3)
    inline_btn_1 = InlineKeyboardButton('Знаю', callback_data='button1')
    inline_btn_2 = InlineKeyboardButton('Не знаю', callback_data='button2')
    inline_btn_3 = InlineKeyboardButton('Пропустить', callback_data='button3')
    inline_kb_full.add(inline_btn_1, inline_btn_2, inline_btn_3)
    return inline_kb_full


def generate_type_training():
    inline_kb_full = InlineKeyboardMarkup(row_width=2)
    inline_btn_1 = InlineKeyboardButton('En-RUS', callback_data='button1')
    inline_btn_2 = InlineKeyboardButton('RUS-EN', callback_data='button2')
    inline_kb_full.add(inline_btn_1, inline_btn_2)
    return inline_kb_full


def generate_know_training():
    inline_kb_full = InlineKeyboardMarkup(row_width=2)
    inline_btn_1 = InlineKeyboardButton('Знаю', callback_data='know1')
    inline_btn_2 = InlineKeyboardButton('Дальше', callback_data='know2')
    inline_kb_full.add(inline_btn_1, inline_btn_2)
    return inline_kb_full