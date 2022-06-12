from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from util.keyboard import generate_type_training, generate_know_training
from words import DataSet, NewWord
from check_answer import check_answer


class ShowWords(StatesGroup):
    train_words = State()


async def start_train_words(message: types.Message):
    keyword = generate_type_training()
    await message.answer(f'Выберите тип тренировки', reply_markup=keyword)


async def process_callback_type_train(callback_query: types.CallbackQuery, state: FSMContext):
    await ShowWords.train_words.set()
    dataset = DataSet(callback_query.from_user.id, callback_query.data)
    new_word = dataset.get_new_word()
    await state.update_data(dataset=dataset, new_word=new_word)
    await callback_query.message.answer(f'Как переводится слово: {new_word.word}')


async def train_words(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    response = check_answer(message.text.lower(), user_data['new_word'])
    if response.answer_result == 1 or response.answer_result == 3:
        dataset = user_data['dataset']
        dataset.save_word(response)
        new_word = dataset.get_new_word()
        await state.update_data(dataset=dataset, new_word=new_word)
        if new_word is not None:
            await message.answer(f'Как переводится слово: {new_word.word}')
        else:
            dataset.save_data_set()
            await state.finish()
            await message.answer(f'Training done')
    elif response.answer_result == 4:
        keyboard = generate_know_training()
        await message.answer('Верно', reply_markup=keyboard)
    else:
        await message.answer(f'Try again')


async def process_callback_know_train(callback_query: types.CallbackQuery, state: FSMContext):
    user_choice = callback_query.data[-1]
    user_data = await state.get_data()
    dataset = user_data['dataset']
    new_word = user_data['new_word']
    stage = 1 if user_choice == '1' else 0
    dataset.save_word(NewWord(word_id=new_word.word_id, true_answer=new_word.true_answer,
                              false_answer=new_word.false_answer, stage=stage, word=new_word.word,
                              word_translate=new_word.word_translate, answer_result=0))
    new_word = dataset.get_new_word()
    await state.update_data(dataset=dataset, new_word=new_word)
    if new_word is not None:
        await callback_query.message.answer(f'Как переводится слово: {new_word.word}')
    else:
        dataset.save_data_set()
        await callback_query.message.answer(f'Training done')
        await state.finish()


def register_handlers_training(dp: Dispatcher):
    dp.register_message_handler(start_train_words, commands="training", state="*")
    dp.register_callback_query_handler(process_callback_type_train, lambda c: c.data and c.data.startswith('button'),
                                        state='*')
    dp.register_callback_query_handler(process_callback_know_train, lambda c: c.data and c.data.startswith('know'),
                                        state=ShowWords.train_words)
    dp.register_message_handler(train_words, state=ShowWords.train_words)