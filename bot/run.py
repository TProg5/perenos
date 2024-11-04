import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession

from bot.Middlewares.Middlewares import ThrottlingMiddleware, CheckAdminMiddleware, BadWordsMiddleware
from bot.moderation_commands import moderation
from other import bad_words

dp = Dispatcher()

session = AiohttpSession()
bot = Bot(token='7245636445:AAF1YxQo3ZDXvnRM381SYsUfbGBVRYbzE54', session=session)


dp.message.middleware(CheckAdminMiddleware(bot))
dp.message.outer_middleware(BadWordsMiddleware(bot, bad_words, 30))
dp.message.middleware(ThrottlingMiddleware())

dp.include_router(moderation)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        print('Бот включается')
        logging.basicConfig(level=logging.INFO)
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f'Бот выключается')
