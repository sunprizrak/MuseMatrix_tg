from aiogram.fsm.state import StatesGroup, State

from keyboards import cansel_form_kb


class LoginForm(StatesGroup):
    email = State()
    password = State()

    params = {
        'email': {
            'quest': 'Write your Email ⬇️',
            'keyboard': lambda: cansel_form_kb(),
        },
        'password': {
            'quest': 'Write your Password ⬇️',
        }
    }


class RegistrateForm(StatesGroup):
    email = State()
    password = State()
    re_password = State()

    params = {
        'email': {
            'quest': 'Write your Email ⬇️',
            'keyboard': lambda: cansel_form_kb(),
        },
        'password': {
            'quest': 'Create a password ⬇️',
        },
        're_password': {
            'quest': 'Repeat password ⬇️',
        },
    }