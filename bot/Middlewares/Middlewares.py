from datetime import datetime, timedelta
from typing import Any, Callable, Dict, Awaitable, List

from aiogram import BaseMiddleware
from aiogram.types import ChatMember
from aiogram.types import Message, ChatPermissions
from cachetools import TTLCache

from Data.requests import add_user
from Data.requests import check_warns, add_warn
from other import word_morphy


class CheckAdminMiddleware(BaseMiddleware):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()

    async def check_admin(self, chat_id: int, user_id: int):
        member: ChatMember = await self.bot.get_chat_member(chat_id=chat_id, user_id=user_id)
        return member.status in ['administrator', 'creator']

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        if not await self.check_admin(event.chat.id, event.from_user.id):
            await event.reply('You are not a group administrator')
            return

        return await handler(event, data)


class BadWordsMiddleware(BaseMiddleware):
    def __init__(self, bot, bad_word: List[str], time: int):
        self.bot = bot
        self.bad_word = bad_word
        self.time = datetime.now() + timedelta(minutes=time)
        super().__init__()

    async def mute_user(self, chat_id, user_id):
        await self.bot.restrict_chat_member(
            chat_id=chat_id,
            user_id=user_id,
            permissions=ChatPermissions(can_send_messages=False),
            until_date=self.time
        )

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:

        for word in event.text.lower().split():
            word = word_morphy(word)

            if word in self.bad_word:
                await add_user(event.from_user.id)

                await add_warn('+', 1, event.from_user.id)

                warns = await check_warns(event.from_user.id)

                if warns == 3:
                    await event.reply(f'{event.from_user.first_name} - has been muted')
                    await add_warn('-', 3, event.from_user.id)
                    await self.mute_user(event.chat.id, event.from_user.id)
                else:
                    await event.reply(f"<b>{event.from_user.first_name}</b> don't swear!\nWarns: {warns} / 3",
                                      parse_mode='HTML')

        return await handler(event, data)


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, limit: int = 5) -> None:
        super().__init__()
        self.limit = TTLCache(maxsize=10000, ttl=limit)

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:

        if event.chat.id in self.limit:
            return
        else:
            self.limit[event.chat.id] = None
        return await handler(event, data)
