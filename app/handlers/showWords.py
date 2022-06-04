from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from db import *
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from play import *

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
    #data = fetch_limit('words',['word','word_translate', 'id'], 'category_id', code, 10)
    #fetch_left_join
    #await callback_query.message.answer(str(callback_query.from_user.id))
    data = fetch_new_words('words', ['id', 'word','word_translate'], 10, str(callback_query.from_user.id), code)
    await state.update_data(data_set=data, counter=1)
    await callback_query.message.answer('Смотрим незнакомые слова')
    inline_kb_full = InlineKeyboardMarkup(row_width=2)
    inline_btn_1 = InlineKeyboardButton('Знаю', callback_data='button1')
    inline_btn_2 = InlineKeyboardButton('Не знаю', callback_data='button2')
    inline_kb_full.add(inline_btn_1, inline_btn_2)
    await callback_query.answer(show_alert=False)
    # await generate_audio(data[0]["word"])
    file_path = f'audio/{data[0]["word"]}.mp3'

    await callback_query.message.answer_voice(voice=open(file_path, "rb"), caption=f'Cлово: {data[0]["word"]}', reply_markup=inline_kb_full)
    #await callback_query.message.answer(f'Cлово: {data[0]["word"]}', reply_markup=inline_kb_full)


async def start_train_words(message: types.Message):
    inline_kb_full = InlineKeyboardMarkup(row_width=2)
    inline_btn_1 = InlineKeyboardButton('En-RUS', callback_data='button1')
    inline_btn_2 = InlineKeyboardButton('RUS-EN', callback_data='button2')
    inline_kb_full.add(inline_btn_1, inline_btn_2)
    await message.answer(f'Выберите тип тренировки', reply_markup=inline_kb_full)


async def process_callback_type_train(callback_query: types.CallbackQuery, state: FSMContext):
    code = callback_query.data[-1]
    await ShowWords.train_words.set()
    train_words_data = fetch_limit('users_words', ['word_id', 'true_answer', 'false_answer', 'stage'], 'user_id', str(callback_query.from_user.id),10)
    await state.update_data(code=code, user_data=train_words_data, counter=0)
    word_data = fetch_where('words', ['word','word_translate'],'id',train_words_data[0]['word_id'])
    word = word_data[0]['word'] if code == '1' else word_data[0]['word_translate']
    await callback_query.message.answer(f'Как переводится слово: {word}')


async def train_words(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    cnt = user_data['counter']
    code = user_data['code']
    word_id = user_data['user_data'][cnt]['word_id']
    word_data = fetch_where('words', ['word', 'word_translate'], 'id', word_id)
    #translate = user_data['user_data'][cnt]['word_translate']
    #word = user_data['user_data'][cnt]['word']
    word = word_data[0]['word'] if code == '1' else word_data[0]['word_translate']
    translate = word_data[0]['word_translate'] if code == '1' else word_data[0]['word']
    if user_data['counter'] < len(user_data['user_data'])-1:
        if str(message.text.lower()) in translate.split(','): # Or all message translate1, translate2
            cnt += 1
            await state.update_data(counter=cnt)
            word_id = user_data['user_data'][cnt]['word_id']
            word_data = fetch_where('words', ['word', 'word_translate'], 'id', word_id)
            word = word_data[0]['word'] if code == '1' else word_data[0]['word_translate']
            #translate = word_data[0]['word_translate'] if code == '1' else word_data[0]['word']
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
    insert('users_words', {'word_id': new_word, 'user_id': call.from_user.id, 'stage': 1})
    if user_data['counter'] < len(user_data['data_set']):
        cnt = user_data['counter']
        word = user_data['data_set'][cnt]['word']
        #update_columns('words', 'stage', 'word', word, '1')
        inline_kb_full = InlineKeyboardMarkup(row_width=2)
        inline_btn_1 = InlineKeyboardButton('Знаю', callback_data='button1')
        inline_btn_2 = InlineKeyboardButton('Не знаю', callback_data='button2')
        inline_kb_full.add(inline_btn_1, inline_btn_2)
        file_path = f'audio/{word}.mp3'
        #await call.message.answer_voice(open(file_path, "rb"))
        #await call.message.answer(f'Cлово: {word}', reply_markup=inline_kb_full)
        await call.message.answer_voice(voice=open(file_path, "rb"), caption=f'Cлово: {word}',
                                                  reply_markup=inline_kb_full)
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
    new_word = user_data['data_set'][cnt - 1]['id']
    insert('users_words', {'word_id': new_word, 'user_id': call.from_user.id})
    #update_columns('words', 'stage','word',word,1)
    if user_data['counter'] < len(user_data['data_set']):
        cnt = user_data['counter']
        word = user_data['data_set'][cnt]['word']
        #update_columns('words', 'stage', 'word', word, '1')
        inline_kb_full = InlineKeyboardMarkup(row_width=2)
        inline_btn_1 = InlineKeyboardButton('Знаю', callback_data='button1')
        inline_btn_2 = InlineKeyboardButton('Не знаю', callback_data='button2')
        inline_kb_full.add(inline_btn_1, inline_btn_2)
        file_path = f'audio/{word}.mp3'

        #await call.message.answer_voice(open(file_path, "rb"))
        #await call.message.answer(f'Cлово: {word}', reply_markup=inline_kb_full)
        await call.message.answer_voice(voice=open(file_path, "rb"), caption=f'Cлово: {word}',
                                        reply_markup=inline_kb_full)

        cnt += 1
        await state.update_data(counter=cnt)
    else:
        await call.message.answer('Приступаем к тренировке')
        await state.finish()
    await call.answer(show_alert=False)





def register_handlers_words(dp: Dispatcher):
    dp.register_message_handler(start_show_words, commands="words", state="*")
    dp.register_message_handler(start_train_words, commands="train", state="*")
    #train_words
    dp.register_message_handler(train_words, state=ShowWords.train_words)
    dp.register_message_handler(show_words, commands="show", state="*")
    dp.register_callback_query_handler(know_btn, lambda c: c.data == 'button1', state=ShowWords.show_words)
    dp.register_callback_query_handler(dont_know_btn, lambda c: c.data == 'button2', state=ShowWords.show_words)
    dp.register_callback_query_handler(process_callback_cat, lambda c: c.data and c.data.startswith('cat'), state="*")
    #process_callback_type_train
    dp.register_callback_query_handler(process_callback_type_train, lambda c: c.data and c.data.startswith('button'), state="*")