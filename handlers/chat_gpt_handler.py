from typing import Any
from aiogram import Router
from aiogram.types import Message

from bot import get_bot
from database import db_read
from api.open_ai import chat_completion
from middlewares import CheckAuthMiddleware


bot = get_bot()
chat_gpt_router = Router()

chat_gpt_router.message.middleware(CheckAuthMiddleware())


@chat_gpt_router.message()
async def message_handler(message: Message) -> Any:
    await bot.send_chat_action(message.chat.id, 'typing')
    user_id = message.from_user.id

    auth_token = await db_read(tg_id=user_id)
    response = await chat_completion(prompt=message.text, auth_token=auth_token)

    if 'message' in response:
        await message.answer(
            text=response.get('message'),
        )