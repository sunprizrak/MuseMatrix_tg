import logging
from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from controller.user_controller import UserController
from keyboards import auth_kb


main_router = Router()


@main_router.message(Command('start'))
async def cmd_start(message: types.Message):
    await message.answer(
        text=f"Hello, {message.from_user.full_name}",
        reply_markup=auth_kb(),
    )
    tg_id = message.from_user.id
    user_controller = UserController(tg_id=tg_id)
    await user_controller.create()


@main_router.message(F.text == 'CANCELLED')
async def cansel_form(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()

    if current_state is None:
        return

    logging.info(f'Cancelling state {current_state}')

    await state.clear()
    await message.answer(
        text='Cancelled.',
        reply_markup=auth_kb(),
    )

