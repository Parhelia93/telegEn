from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from db import *
from util.keyboard import generate_type_training


class ShowWords(StatesGroup):
    train_words = State()


async def start_train_words(message: types.Message):
    keyword = generate_type_training()
    await message.answer(f'Выберите тип тренировки', reply_markup=keyword)


async def train_words(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    cnt = user_data['counter']
    code = user_data['code']
    word_id = user_data['user_data'][cnt]['word_id']
    word_data = fetch_where('words', ['word', 'word_translate'], 'id', word_id)
    translate = word_data[0]['word_translate'] if code == '1' else word_data[0]['word']
    wrong_answer = user_data['wrongAnser']
    if user_data['counter'] < len(user_data['user_data'])-1:
        if str(message.text.lower()) in translate.split(',') and wrong_answer<3:
            cnt += 1
            await state.update_data(wrongAnser=0)
            await state.update_data(counter=cnt)
            word_id = user_data['user_data'][cnt]['word_id']
            word_data = fetch_where('words', ['word', 'word_translate'], 'id', word_id)
            word = word_data[0]['word'] if code == '1' else word_data[0]['word_translate']
            await message.answer(f'Правильно. Как переводится: {word}')
        elif wrong_answer==3:
            await message.answer(f'Перевод: {translate}')
            await state.update_data(wrongAnser=0)
            cnt += 1
            await state.update_data(counter=cnt)
            word_id = user_data['user_data'][cnt]['word_id']
            word_data = fetch_where('words', ['word', 'word_translate'], 'id', word_id)
            word = word_data[0]['word'] if code == '1' else word_data[0]['word_translate']
            await message.answer(f'Как переводится: {word}')
        else:
            await message.answer('Wrong, try again')
            wrong_answer+=1
            await state.update_data(wrongAnser=wrong_answer)
    else:
        await message.answer('Тренировка закочена')
        await state.finish()


async def process_callback_type_train(callback_query: types.CallbackQuery, state: FSMContext):
    code = callback_query.data[-1]
    await ShowWords.train_words.set()
    train_words_data = fetch_limit('users_words', ['word_id', 'true_answer', 'false_answer', 'stage'], 'user_id', str(callback_query.from_user.id),10)
    await state.update_data(code=code, user_data=train_words_data, counter=0, wrongAnser=0)
    word_data = fetch_where('words', ['word','word_translate'],'id',train_words_data[0]['word_id'])
    word = word_data[0]['word'] if code == '1' else word_data[0]['word_translate']
    await callback_query.message.answer(f'Как переводится слово: {word}')


def register_handlers_training(dp: Dispatcher):
    dp.register_message_handler(start_train_words, commands="training", state="*")
    dp.register_callback_query_handler(process_callback_type_train, lambda c: c.data and c.data.startswith('button'),
                                       state='*')
    dp.register_message_handler(train_words, state=ShowWords.train_words)