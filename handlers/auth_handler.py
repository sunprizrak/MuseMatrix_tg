from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from controller.user_controller import UserController
from keyboards import auth_kb
from states import LoginForm, RegistrateForm

auth_router = Router()


@auth_router.message(F.text == 'REGISTRATE')
async def open_registration_form(message: types.Message, state: FSMContext) -> None:
    await state.set_state(RegistrateForm.email)
    await message.answer(
        text=RegistrateForm.params['email']['quest'],
        reply_markup=RegistrateForm.params['email']['keyboard'](),
    )


@auth_router.message(RegistrateForm.email)
async def process_email(message: types.Message, state: FSMContext) -> None:
    await state.update_data(email=message.text)
    await state.set_state(RegistrateForm.password)
    await message.answer(
        text=RegistrateForm.params['password']['quest'],
    )


@auth_router.message(RegistrateForm.password)
async def process_password(message: types.Message, state: FSMContext) -> None:
    await state.update_data(password=message.text)
    await state.set_state(RegistrateForm.re_password)
    await message.answer(
        text=RegistrateForm.params['re_password']['quest'],
    )


@auth_router.message(RegistrateForm.re_password)
async def process_password(message: types.Message, state: FSMContext) -> None:
    await state.update_data(re_password=message.text)

    data = await state.get_data()

    tg_id = message.from_user.id
    user_controller = UserController(tg_id=tg_id)

    response = await user_controller.registrate(
        email=data.get('email'),
        password=data.get('password'),
        re_password=data.get('re_password'),
    )

    if type(response) != dict:
        await message.answer(
            text=f"Activation email has been sent to your email {data.get('email')}, confirm your email to login continue.",
            reply_markup=auth_kb(),
        )

        await state.clear()
    elif type(response) == dict:
        if 'email' in response:
            await state.set_state(RegistrateForm.email)
            for error in response['email']:
                await message.answer(
                    text=f'- {error}',
                )
            await message.answer(
                text=RegistrateForm.params['email']['quest'],
            )
        else:
            if 'password' in response:
                await state.set_state(RegistrateForm.password)
                for error in response['password']:
                    await message.answer(
                        text=f'- {error}',
                    )
                await message.answer(
                    text=RegistrateForm.params['password']['quest'],
                )
            else:
                if 'non_field_errors' in response:
                    await state.set_state(RegistrateForm.password)
                    for error in response['non_field_errors']:
                        await message.answer(
                            text=f'- {error}',
                        )
                    await message.answer(
                        text=RegistrateForm.params['password']['quest'],
                    )


@auth_router.message(F.text == 'LOGIN')
async def open_login_form(message: types.Message, state: FSMContext) -> None:
    await state.set_state(LoginForm.email)
    await message.answer(
        text=LoginForm.params['email']['quest'],
        reply_markup=LoginForm.params['email']['keyboard'](),
    )


@auth_router.message(LoginForm.email)
async def process_email(message: types.Message, state: FSMContext) -> None:
    await state.update_data(email=message.text)
    await state.set_state(LoginForm.password)
    await message.answer(
        text=LoginForm.params['password']['quest'],
    )


@auth_router.message(LoginForm.password)
async def process_password(message: types.Message, state: FSMContext) -> None:
    await state.update_data(password=message.text)

    data = await state.get_data()

    tg_id = message.from_user.id
    user_controller = UserController(tg_id=tg_id)

    response = await user_controller.authentication(
        email=data.get('email'),
        password=data.get('password'),
    )

    if type(response) != dict:
        await message.answer(
            text='Authorization success! Нou can start chatting.',
            reply_markup=ReplyKeyboardRemove(),
        )

        await state.clear()
    elif type(response) == dict:
        if 'non_field_errors' in response:
            await state.set_state(LoginForm.email)
            for error in response['non_field_errors']:
                await message.answer(
                    text=f'- {error}',
                )
            await message.answer(
                text=LoginForm.params['email']['quest'],
            )

