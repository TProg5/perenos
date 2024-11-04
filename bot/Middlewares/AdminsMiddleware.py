from typing import Any, Callable, Dict, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import ChatMember
from aiogram.types import Message


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
            await event.reply('Вы не являетесь администратором группы')
            return
        else:
            return await handler(event, data)
