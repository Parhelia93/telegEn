from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from db import *
from util.keyboard import generate_keyboard


class ShowWords(StatesGroup):
    show_words = State()


async def start_show_words(message: types.Message):
    user_data = fetchall('wordCategory', ['id', 'category_name'])
    result = 'У вас есть следующие категории слов:\n'
    for i in user_data:
        cat_id = f'Категория:\t{i["category_name"]}\tссылка:\t/cat{i["id"]}\n'
        result += cat_id
    await message.answer(result)


async def chose_cat(message: types.Message, state: FSMContext):
    code = int(message.text.replace('/cat', ''))
    await ShowWords.show_words.set()
    data = fetch_new_words('words', ['id', 'word','word_translate'], 10, str(message.from_user.id), code)
    await state.update_data(data_set=data, counter=1)
    keyboard = generate_keyboard()
    file_path = f'audio/{data[0]["word"]}.mp3'
    try:
        await message.answer_voice(voice=open(file_path, "rb"), caption=f'Cлово: {data[0]["word"]}', reply_markup=keyboard)
    except:
        await message.answer(f'Cлово: {data[0]["word"]}', reply_markup=keyboard)


async def chose_word_result(call: types.CallbackQuery, state: FSMContext):
    code = call.data[-1]
    user_data = await state.get_data()
    cnt = user_data['counter']
    new_word = user_data['data_set'][cnt - 1]['id']
    if code == '1':
        insert('users_words', {'word_id': new_word, 'user_id': call.from_user.id, 'stage': 1})
    elif code == '2':
        insert('users_words', {'word_id': new_word, 'user_id': call.from_user.id})
    if user_data['counter'] < len(user_data['data_set']):
        word = user_data['data_set'][cnt]['word']
        keyword = generate_keyboard()
        file_path = f'audio/{word}.mp3'
        try:
            await call.message.answer_voice(voice=open(file_path, "rb"), caption=f'Cлово: {word}',
                                        reply_markup=keyword)
        except:
            await call.message.answer(f'Cлово: {word}',
                                        reply_markup=keyword)
        cnt += 1
        await state.update_data(counter=cnt)
    else:
        await call.message.answer('Приступаем к тренировке')
        await state.finish()
    await call.answer(show_alert=False)


def register_handlers_words(dp: Dispatcher):
    dp.register_message_handler(start_show_words, commands="words", state="*")
    dp.register_callback_query_handler(chose_word_result, lambda c: c.data and c.data.startswith('button'),
                                       state=ShowWords.show_words)
    dp.register_message_handler(chose_cat, lambda message: message.text.startswith('/cat'), state="*")
