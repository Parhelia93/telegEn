"""
/w word - check words in table words, if word contain in db, show words with translate, show btn add word to user_words
table, if don't contain err message(I don't know this word)

/learned - show all user words with stage 1
"""

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from db import *


async def search_word(message: types.Message, state: FSMContext):
    await state.finish()
    user_id = message.from_user.id
    word = f"'{message.text.replace('/w', '').strip()}'"
    data = fetch_where('words', ['word', 'word_translate'], 'word', word)
    if len(data) != 0:
        file_path = f'audio/{data[0]["word"]}.mp3'
        try:
            await message.answer_voice(voice=open(file_path, "rb"), caption=f'Cлово: {data[0]["word"]} - {data[0]["word_translate"]}')
        except:
            await message.answer('Что-то пошло не так...')

    else:
        await message.answer('В словаре нет такого слова')


async def cmd_show_learned_words(message: types.Message, state: FSMContext):
    await state.finish()
    msg = 'Изученные слова:\n'
    user_id = message.from_user.id
    data = fetch_learned_words('users_words', ['word_id', 'true_answer'], user_id)
    for i in data:
        description_word = fetch_where('words', ['word', 'word_translate'], 'id', i['word_id'])
        ms = f"{description_word[0]['word']} - {description_word[0]['word_translate']}\n"
        msg+=ms
    await message.answer(msg)


def register_handlersquick_cmd(dp: Dispatcher):
    dp.register_message_handler(search_word, lambda message: message.text.startswith('/w'), state="*")
    dp.register_message_handler(cmd_show_learned_words, commands="learned", state="*")