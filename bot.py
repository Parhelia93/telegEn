import asyncio
import logging

from aiogram.types import BotCommand
from aiogram import Bot, Dispatcher


from aiogram.contrib.fsm_storage.memory import MemoryStorage
from app.config_reader import load_config
from app.handlers.showWords import register_handlers_words
from app.handlers.common import register_handlers_common
logger = logging.getLogger(__name__)


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/words", description="Слова")
    ]
    await bot.set_my_commands(commands)


async def main():
    # Настройка логирования в stdout
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger.error("Starting bot")

    # Парсинг файла конфигурации
    config = load_config("config/bot.ini")

    # Объявление и инициализация объектов бота и диспетчера
    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher(bot, storage=MemoryStorage())

    # Регистрация хэндлеров
    register_handlers_words(dp)
    register_handlers_common(dp)
    # Установка команд бота
    await set_commands(bot)

    # Запуск поллинга
    # await dp.skip_updates()  # пропуск накопившихся апдейтов (необязательно)
    await dp.start_polling()



if __name__ == '__main__':
    asyncio.run(main())