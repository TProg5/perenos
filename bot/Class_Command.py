from aiogram.types import ChatPermissions

from Data.requests import check_warns, add_warn
from mute_commands import parse_time


class ModerationCommands:
    def __init__(self, bot, message, message_id, user_id,
                 user_name):
        self.bot = bot
        self.message = message
        self.message_id = message_id
        self.user_id = user_id
        self.user_name = user_name

    async def ban(self):
        await self.bot.ban_chat_member(self.message_id, self.user_id)
        await self.message.reply(f"User {self.user_name} has been baned")

    async def mute_user(self, time):
        time_mute, mute_text, num_mute = await parse_time(time)

        await self.bot.restrict_chat_member(
            chat_id=self.message.chat.id,
            user_id=self.message.reply_to_message.from_user.id,
            until_date=time_mute,
            permissions=ChatPermissions(can_send_messages=False, can_send_photos=False, can_send_videos=False)
        )
        await self.message.reply(
            f"User @{self.message.reply_to_message.from_user.first_name} has been muted for <b>{num_mute}"
            f"</b> {mute_text}\nAdmin: <b>@{self.message.from_user.username}</b>\n",
            parse_mode='HTML')

    async def warn(self):
        await add_warn('+', 1, self.message.from_user.id)

        warns = await check_warns(self.message.from_user.id)

        if warns == 3:
            await mute_user(self.message.chat.id, self.message.from_user.id)
            await self.message.reply(f'{self.message.from_user.first_name} has been muted')
            await add_warn('+', 1, self.message.from_user.id)
        else:
            await self.message.reply(f'<b>{self.message.from_user.first_name}</b> - get warn\nWarns: {warns} / 3',
                                     parse_mode='HTML')
