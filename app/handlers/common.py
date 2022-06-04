from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text, IDFilter
from db import *


async def cmd_start(message: types.Message, state: FSMContext):
    await state.finish()
    user_id = message.from_user.id
    data = fetch_where('users', ['users_id'], 'users_id', user_id)
    if len(data) == 0:
        insert('users', {'users_id':user_id})
    await message.answer(
        "Hellow, we have this commands: words (/words) and help (/show_words).",
        reply_markup=types.ReplyKeyboardRemove()
    )



async def process_voice_command(message: types.Message):
    await message.answer_voice('AwACAgIAAxkDAAIF9mKbb02Pp8rg01L_KTbBBArkkj-lAAKfGgACTyDgSPxoa4q8x8wZJAQ')


def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands="start", state="*")
    dp.register_message_handler(process_voice_command, commands="voice", state='*')