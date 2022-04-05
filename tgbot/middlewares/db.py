from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware


class DbMiddleware(LifetimeControllerMiddleware):
    skip_patterns = ["error", "update"]

    async def pre_process(self, obj, data, *args):
        # db_session = obj.bot.get('db')
        # data['db_session'] = db_session
        config = obj.bot.get('config')
        data['config'] = config
        # scheduler = obj.bot.get('scheduler')
        # data['scheduler'] = scheduler
