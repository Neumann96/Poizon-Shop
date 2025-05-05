from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_ikb_start():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text='🎁 Оформить заказ ❤️', callback_data='make_order'),
                InlineKeyboardButton(text='💰 Калькулятор стоимости', callback_data='what'),
                InlineKeyboardButton(text='💬 Отзывы о нашей работе', url=''),
                InlineKeyboardButton(text='📚 Ответы на популярные вопросы', callback_data='what'),
                InlineKeyboardButton(text='📡 Отследить посылку', url=''),
                InlineKeyboardButton(text='🧾 Задать вопрос', url=''),
                InlineKeyboardButton(text='🏙️ Скачать POIZON iOS', url=''),
                InlineKeyboardButton(text='📱 Скачать POIZON Android', url=''),)
    return builder.as_markup()