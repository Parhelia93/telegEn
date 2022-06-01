from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from db import *
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton


class ShowWords(StatesGroup):
    train_words = State()
    show_words = State()


async def start_show_words(message: types.Message):

    # user_data = fetch_limit('words', ['word', 'word_traslate'],
    #                         'stage', '0', '10')
    # await state.update_data(data_set=user_data, counter=0)
    # await message.answer(f'Как переводится слово: {user_data[0]["word"]}')
    inline_kb_full = InlineKeyboardMarkup(row_width=2)
    user_data = fetchall('wordCategory', ['id', 'category_name'])

    for i in user_data:
        cat_id = f'cat{i["id"]}'
        #await message.answer(cat_id)
        inline_kb_full.add(InlineKeyboardButton(i['category_name'], callback_data=cat_id))
    await message.answer(f'Есть следующие категории слов', reply_markup=inline_kb_full)
    #await ShowWords.train_words.set()


async def process_callback_cat(callback_query: types.CallbackQuery, state: FSMContext):
    code = callback_query.data[-1]
    await ShowWords.show_words.set()
    data = fetch_limit('words',['word','word_translate', 'id'], 'category_id', code, 10)

    await state.update_data(data_set=data, counter=1)
    await callback_query.message.answer('Смотрим незнакомые слова')
    inline_kb_full = InlineKeyboardMarkup(row_width=2)
    inline_btn_1 = InlineKeyboardButton('Знаю', callback_data='button1')
    inline_btn_2 = InlineKeyboardButton('Не знаю', callback_data='button2')
    inline_kb_full.add(inline_btn_1, inline_btn_2)
    await callback_query.answer(show_alert=False)
    await callback_query.message.answer(f'Cлово: {data[0]["word"]}', reply_markup=inline_kb_full)



async def train_words(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    cnt = user_data['counter']
    translate = user_data['data_set'][cnt]['word_traslate']
    if user_data['counter'] < len(user_data['data_set'])-1:
        if str(message.text.lower()) in translate.split(','): # Or all message translate1, translate2
            cnt += 1
            await state.update_data(counter=cnt)
            word = user_data['data_set'][cnt]['word']
            await message.answer(f'Правильно. Как переводится: {word}')
        else:
            await message.answer('Wrong, try again')
    else:
        await message.answer('Тренировка закочена')
        await state.finish()


async def show_words(message: types.Message, state: FSMContext):
    await message.answer('Смотрим незнакомые слова')
    user_data = fetch_limit('words', ['word', 'word_traslate'],
                            'stage', '0', '10')
    inline_kb_full = InlineKeyboardMarkup(row_width=2)
    inline_btn_1 = InlineKeyboardButton('Знаю', callback_data='button1')
    inline_btn_2 = InlineKeyboardButton('Не знаю', callback_data='button2')
    inline_kb_full.add(inline_btn_1, inline_btn_2)
    await message.answer(f'Cлово: {user_data[0]["word"]}', reply_markup=inline_kb_full)
    await state.update_data(data_set=user_data, counter=1)
    await ShowWords.show_words.set()



async def know_btn(call: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    cnt = user_data['counter']
    new_word = user_data['data_set'][cnt-1]['id']
    #update_columns('words', 'stage','word',word,1)
    insert('users_words', {'word_id':new_word, 'user_id':call.from_user.id})
    if user_data['counter'] < len(user_data['data_set']):
        cnt = user_data['counter']
        word = user_data['data_set'][cnt]['word']
        #update_columns('words', 'stage', 'word', word, '1')
        inline_kb_full = InlineKeyboardMarkup(row_width=2)
        inline_btn_1 = InlineKeyboardButton('Знаю', callback_data='button1')
        inline_btn_2 = InlineKeyboardButton('Не знаю', callback_data='button2')
        inline_kb_full.add(inline_btn_1, inline_btn_2)
        await call.message.answer(f'Cлово: {word}', reply_markup=inline_kb_full)
        cnt += 1
        await state.update_data(counter=cnt)
    else:
        await call.message.answer('Приступаем к тренировке')
        await state.finish()
    await call.answer(show_alert=False)

async def dont_know_btn(call: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    cnt = user_data['counter']
    word = user_data['data_set'][cnt-1]['word']
    #update_columns('words', 'stage','word',word,1)
    if user_data['counter'] < len(user_data['data_set']):
        cnt = user_data['counter']
        word = user_data['data_set'][cnt]['word']
        #update_columns('words', 'stage', 'word', word, '1')
        inline_kb_full = InlineKeyboardMarkup(row_width=2)
        inline_btn_1 = InlineKeyboardButton('Знаю', callback_data='button1')
        inline_btn_2 = InlineKeyboardButton('Не знаю', callback_data='button2')
        inline_kb_full.add(inline_btn_1, inline_btn_2)
        await call.message.answer(f'Cлово: {word}', reply_markup=inline_kb_full)
        cnt += 1
        await state.update_data(counter=cnt)
    else:
        await call.message.answer('Приступаем к тренировке')
        await state.finish()
    await call.answer(show_alert=False)





def register_handlers_words(dp: Dispatcher):
    dp.register_message_handler(start_show_words, commands="words", state="*")
    dp.register_message_handler(train_words, state=ShowWords.train_words)
    dp.register_message_handler(show_words, commands="show", state="*")
    dp.register_callback_query_handler(know_btn, lambda c: c.data == 'button1', state=ShowWords.show_words)
    dp.register_callback_query_handler(dont_know_btn, lambda c: c.data == 'button2', state=ShowWords.show_words)
    dp.register_callback_query_handler(process_callback_cat, lambda c: c.data and c.data.startswith('cat'), state="*")