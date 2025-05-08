from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def ikb_come_home():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text='🏠На главную', callback_data='home'))
    return builder.as_markup()


def get_ikb_start():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text='🧾 Оформить заказ', callback_data='make_order'),
                InlineKeyboardButton(text='💵 Рассчитать стоимость', callback_data='calc'),
                InlineKeyboardButton(text='💬 Отзывы', url='https://t.me/pumbafeedbacks'),
                InlineKeyboardButton(text='❓ Частые вопросы', callback_data='often_quest'),
                InlineKeyboardButton(text='📍 Отследить заказ', url='https://t.me/lottematte'),
                InlineKeyboardButton(text='📩 Задать вопрос', url='https://t.me/lottematte'),
                InlineKeyboardButton(text='📲 Скачать POIZON iOS', url='https://apps.apple.com/am/app/%E5%BE%97%E7%89%A9-%E5%BE%97%E5%88%B0%E7%BE%8E%E5%A5%BD%E4%BA%8B%E7%89%A9/id1012871328'),
                InlineKeyboardButton(text='🤖 Скачать POIZON Android', url='https://www.anxinapk.com/rj/12201303.html'),)
    builder.adjust(1)
    return builder.as_markup()


def get_ikb_kat():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text='👟 Кроссовки', callback_data='calc_sneakers'))
    builder.add(InlineKeyboardButton(text='👕 Футболки, шорты', callback_data='calc_shorts'),
                InlineKeyboardButton(text='🥾 Ботинки', callback_data='calc_boots'))
    builder.add(InlineKeyboardButton(text='🧥 Толстовки, кофты, лёгкие куртки', callback_data='calc_hoody'))
    builder.add(InlineKeyboardButton(text='👜 Маленькие сумки', callback_data='calc_small_bag'),
                InlineKeyboardButton(text='🧳 Большие сумки', callback_data='calc_big_bag'))
    builder.add(InlineKeyboardButton(text='🧦 Носки, майки, нижнее бельё', callback_data='calc_socks'))
    builder.add(InlineKeyboardButton(text='👖 Штаны, джинсы', callback_data='calc_jeans'),
                InlineKeyboardButton(text='🧢 Головные уборы', callback_data='calc_hats'))
    builder.add(InlineKeyboardButton(text='🧥 Зимние куртки, пальто', callback_data='calc_jacket'))
    builder.add(InlineKeyboardButton(text='🏠На главную', callback_data='home'))

    builder.adjust(1, 2, 1, 2, 1, 2, 1, 1)
    return builder.as_markup()

