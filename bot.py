import asyncio
import logging
import os
import stun
import django
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from tgbot.config import load_config, load_postgres_URI
from tgbot.filters.admin import AdminFilter
from tgbot.middlewares.db import DbMiddleware
from tgbot.models.gino_PostgreSQL import db, on_startup
from apscheduler.schedulers.asyncio import AsyncIOScheduler

logger = logging.getLogger(__name__)
host = stun.get_ip_info()[1]

def setup_django():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'telegrambot.settings')
    os.environ.update({"DJANGO_ALLOW_ASYNC_UNSAFE": "true"})
    django.setup()


def register_all_middlewares(dp):
    dp.setup_middleware(DbMiddleware())


def register_all_filters(dp):
    dp.filters_factory.bind(AdminFilter)


def register_all_handlers(dp):
    from tgbot.handlers.echo import register_echo
    from tgbot.handlers.user_menu import register_user
    register_user(dp)
    # register_admin(dp)
    register_echo(dp)


async def main():
    setup_django()
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")
    config = load_config(".env")
    postgres_uri = load_postgres_URI(".env")
    scheduler = AsyncIOScheduler()
    storage = RedisStorage2() if config.tg_bot.use_redis else MemoryStorage()
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher(bot, storage=storage)

    await on_startup(db, postgres_uri.postgres_uri)
    bot['config'] = config
    bot['scheduler'] = scheduler
    register_all_middlewares(dp)
    register_all_filters(dp)
    register_all_handlers(dp)

    # start
    try:
        # await db.gino.drop_all()
        await db.gino.create_all()
        scheduler.start()
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
