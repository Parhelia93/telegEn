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


def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands="start", state="*")