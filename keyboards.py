from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_ikb_what():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text='Как этим пользоваться?🤔', callback_data='what'))
    return builder.as_markup()