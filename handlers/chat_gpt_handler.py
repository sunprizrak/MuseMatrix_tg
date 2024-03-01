from typing import Any, Dict

from aiogram import Router
from aiogram.types import Message

from middlewares import CheckAuthMiddleware

chat_gpt_router = Router()


chat_gpt_router.message.middleware(CheckAuthMiddleware())


@chat_gpt_router.message()
async def message_handler(message: Message) -> Any:
    await message.answer('Hello from my router!')