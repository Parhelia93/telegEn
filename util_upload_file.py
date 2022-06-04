import os
import asyncio
import logging
from aiogram import Bot
from db import *
bot = Bot(token='5372120570:AAGKSmF9UYftARHQrsmv19V_R7EdVGiSGSs')

BASE_MEDIA_PATH = './audio'

logging.basicConfig(format=u'%(filename)s [ LINE:%(lineno)+3s ]#%(levelname)+8s [%(asctime)s]  %(message)s',
                    level=logging.DEBUG)


async def upload_media_files(method, file_attr):
    for filename in os.listdir(BASE_MEDIA_PATH):
        logging.info(filename)
        with open(os.path.join(BASE_MEDIA_PATH, filename), 'rb') as file:
            msg = await method('132166344', file, disable_notification=True)
            file_id = getattr(msg, file_attr).file_id
            logging.info(file_id)
            flr = filename.split('.')
            await asyncio.sleep(1)
            update_columns('words', 'voice_id', 'word', flr[0], file_id)

loop = asyncio.get_event_loop()

tasks = [loop.create_task(upload_media_files(bot.send_voice, 'voice'))]
wait_tasks = asyncio.wait(tasks)
loop.run_until_complete(wait_tasks)
loop.close()

