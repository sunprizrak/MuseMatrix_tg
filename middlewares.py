from typing import Dict, Any, Awaitable, Callable
from controller.user_controller import UserController


from aiogram import BaseMiddleware
from aiogram.types import Message


class CheckAuthMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        user_id = event.from_user.id
        user_controller = UserController(tg_id=user_id)
        auth_token = await user_controller.get_auth_token()
        data['auth_token'] = auth_token
        if auth_token is None:
            await event.reply(
                text="Please login or register.",
            )
            return
        else:
            return await handler(event, data)