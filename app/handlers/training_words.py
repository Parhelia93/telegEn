from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from db import *
from util.keyboard import generate_type_training, generate_know_training


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
    true_answer = user_data['user_data'][cnt]['true_answer']

    if user_data['counter'] < len(user_data['user_data'])-1:
        if str(message.text.lower()) in translate.split(',') and wrong_answer<3:
            cnt += 1
            true_answer+=1
            update_columns_and('users_words', 'true_answer', 'word_id', word_id, true_answer, 'user_id',
                               message.from_user.id)
            await state.update_data(wrongAnser=0)
            await state.update_data(counter=cnt)
            await state.update_data(word_id=word_id)
            word_id = user_data['user_data'][cnt]['word_id']
            word_data = fetch_where('words', ['word', 'word_translate'], 'id', word_id)
            word = word_data[0]['word'] if code == '1' else word_data[0]['word_translate']
            if true_answer < 2:
                await message.answer(f'Правильно. Как переводится: {word}')
            else:
                keyword = generate_know_training()
                await message.answer(f'Правильно.', reply_markup=keyword)

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
    train_words_data = fetch_limit_and('users_words', ['word_id', 'true_answer', 'false_answer', 'stage'], 'user_id',
                                       str(callback_query.from_user.id), 10, 'stage', 0)
    await state.update_data(code=code, user_data=train_words_data, counter=0, wrongAnser=0)
    word_data = fetch_where('words', ['word','word_translate'],'id',train_words_data[0]['word_id'])
    word = word_data[0]['word'] if code == '1' else word_data[0]['word_translate']
    await callback_query.message.answer(f'Как переводится слово: {word}')


async def process_callback_know_train(callback_query: types.CallbackQuery, state: FSMContext):
    user_choice = callback_query.data[-1]
    user_data = await state.get_data()
    cnt = user_data['counter']
    code = user_data['code']
    word_id = user_data['user_data'][cnt]['word_id']
    word_data = fetch_where('words', ['word', 'word_translate'], 'id', word_id)
    translate = word_data[0]['word_translate'] if code == '1' else word_data[0]['word']
    wrong_answer = user_data['wrongAnser']
    true_answer = user_data['user_data'][cnt]['true_answer']
    wrd = user_data['word_id']

    if user_choice == '1':
        await callback_query.message.answer(f'Запомнил. Как переводится: {word_data[0]["word"]}')
        update_columns_and('users_words', 'stage', 'word_id', wrd, 1, 'user_id', callback_query.from_user.id)

    else:
        await callback_query.message.answer(f'Ну ок. Как переводится: {word_data[0]["word"]}')


def register_handlers_training(dp: Dispatcher):
    dp.register_message_handler(start_train_words, commands="training", state="*")
    dp.register_callback_query_handler(process_callback_type_train, lambda c: c.data and c.data.startswith('button'),
                                       state='*')
    dp.register_callback_query_handler(process_callback_know_train, lambda c: c.data and c.data.startswith('know'),
                                       state=ShowWords.train_words)
    dp.register_message_handler(train_words, state=ShowWords.train_words)