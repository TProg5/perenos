from datetime import datetime, timedelta
from typing import Any, Callable, Dict, Awaitable, List

from aiogram import BaseMiddleware
from aiogram.types import Message, ChatPermissions

from Data.requests import add_user
from Data.requests import check_warns, add_warn
from other import word_morphy


class BadWordsMiddleware(BaseMiddleware):
    def __init__(self, bot, bad_word: List[str]):
        self.bot = bot
        self.bad_word = bad_word
        super().__init__()

    async def mute_user(self, chat_id, user_id):
        time = datetime.now() + timedelta(minutes=30)
        await self.bot.restrict_chat_member(
            chat_id=chat_id,
            user_id=user_id,
            permissions=ChatPermissions(can_send_messages=False),
            until_date=time
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
                    await self.mute_user(event.chat.id, event.from_user.id)
                    await event.reply(f'{event.from_user.first_name} - has been muted')
                    await add_warn('-', 3, event.from_user.id)
                else:
                    await event.reply(f"<b>{event.from_user.first_name}</b> don't swear!\nWarns: {warns} / 3",
                                      parse_mode='HTML')
