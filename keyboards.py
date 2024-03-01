from types import FunctionType
from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


def default_inline_kb(buttons: dict, adjust: int | tuple, factory, back_factory=None, back_text=None) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()

    for elem in buttons:

        if isinstance(elem, FunctionType):
            old_elem = elem
            new_elem = elem()
            kb.button(text=new_elem, callback_data=factory(field=buttons[old_elem]))
        else:
            kb.button(text=elem, callback_data=factory(field=buttons[elem]))

    if back_factory and back_text:
        kb.button(text=back_text, callback_data=back_factory)

    if isinstance(adjust, tuple):
        kb.adjust(*adjust)
    elif isinstance(adjust, int):
        kb.adjust(adjust)

    return kb.as_markup(
        resize_keyboard=True,
    )


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