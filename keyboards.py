from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def auth_kb():
    kb = ReplyKeyboardBuilder()

    kb.button(text='LOGIN')
    kb.button(text='REGISTRATE')

    return kb.as_markup(
        resize_keyboard=True,
    )


def cansel_form_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()

    kb.button(text='CANCELLED')

    return kb.as_markup(
        resize_keyboard=True,
    )