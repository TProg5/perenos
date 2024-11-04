import logging

from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.types import Message, ChatPermissions

from Data.requests import check_warns, add_warn
# from time_mute import parse_time, parse_block
from mute_commands import parse_time

moderation = Router()
bot = Bot(token='7245636445:AAF1YxQo3ZDXvnRM381SYsUfbGBVRYbzE54')


async def ban(bot, message, message_id, user_id, user_name):
    await bot.ban_chat_member(message_id, user_id)
    await message.reply(f"User {user_name} has been baned")


@moderation.message(Command('ban', 'бан'))
async def command_mute(message: Message):
    if not message.reply_to_message:
        await message.reply("Ответьте на сообщение пользователя")
        return

    user_id = message.reply_to_message.from_user.id

    try:
        await ban(bot, message, message.chat.id, user_id, message.reply_to_message.from_user.first_name)

    except Exception as e:
        await message.reply("Нельзя забанить админа!")
        logging.error(f"Ошибка бана пользователя: {e}")


@moderation.message(Command('mute', 'мут'))
async def command_mute(message: Message):
    if not message.reply_to_message:
        await message.reply("Ответьте на сообщение пользователя")
        return

    time_mute, mute_text, num_mute = await parse_time(message.text)

    try:
        await bot.restrict_chat_member(
            chat_id=message.chat.id,
            user_id=message.reply_to_message.from_user.id,
            until_date=time_mute,
            permissions=ChatPermissions(can_send_messages=False, can_send_photos=False, can_send_videos=False)
        )
        await message.reply(
            f"User @{message.reply_to_message.from_user.first_name} has been muted for <b>{num_mute}"
            f"</b> {mute_text}\nAdmin: <b>@{message.from_user.username}</b>\n",
            parse_mode='HTML')
    except Exception as e:
        await message.reply("Нельзя замутить админа")
        logging.error(f"Ошибка мута пользователя: {e}")


@moderation.message(Command('warn', 'варн'))
async def warn(message: Message):
    if not message.reply_to_message:
        await message.reply("Ответьте на сообщение пользователя")
        return

    await add_warn('+', 1, message.from_user.id)

    warns = await check_warns(message.from_user.id)

    if warns == 3:
        await mute_user(message.chat.id, message.from_user.id)
        await message.reply(f'{message.from_user.first_name} - закройка ебало')
        await add_warn('+', 1, message.from_user.id)
    else:
        await message.reply(f'<b>{message.from_user.first_name}</b> - живи пока\nWarns: {warns} / 3',
                            parse_mode='HTML')
