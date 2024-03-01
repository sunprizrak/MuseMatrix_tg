from typing import Dict, Any, Awaitable, Callable
from aiogram import BaseMiddleware
from aiogram.types import Message
from database import db_read


class CheckAuthMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        user_id = event.from_user.id
        auth_token = await db_read(tg_id=user_id)
        data['auth_token'] = auth_token
        if auth_token is None:
            await event.reply(
                text="Please login or register.",
            )
            return
        else:
            return await handler(event, data)