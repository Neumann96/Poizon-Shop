from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
import sqlite3


def ikb_come_home():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text='🏠 На главную', callback_data='home'))
    return builder.as_markup()


def ikb_home_order():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text='🏠 На главную', callback_data='home'),
                InlineKeyboardButton(text='🧾 Оформить заказ', callback_data='make_order'))
    return builder.as_markup()


def get_ikb_start():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text='💵 Рассчитать стоимость', callback_data='calc'),
                InlineKeyboardButton(text='🧾 Оформить заказ', callback_data='make_order'),
                InlineKeyboardButton(text='💬 Отзывы', url='https://t.me/pumbafeedbacks'),
                InlineKeyboardButton(text='📖 Инструкция', callback_data='instructions'),
                InlineKeyboardButton(text='❓ Частые вопросы', callback_data='often_quest'),
                InlineKeyboardButton(text='📩 Задать вопрос', url='https://t.me/lottematte'),
                InlineKeyboardButton(text='📲 Скачать POIZON iOS', url='https://apps.apple.com/am/app/%E5%BE%97%E7%89%A9-%E5%BE%97%E5%88%B0%E7%BE%8E%E5%A5%BD%E4%BA%8B%E7%89%A9/id1012871328'),
                InlineKeyboardButton(text='🤖 Скачать POIZON Android', url='https://www.dewu.com/'),)
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
    builder.add(InlineKeyboardButton(text='🏠 На главную', callback_data='home'))

    builder.adjust(1, 2, 1, 2, 1, 2, 1, 1)
    return builder.as_markup()


def ikb_often_question():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text='Какие сроки доставки?', callback_data='time_delivery'),
                InlineKeyboardButton(text='Какой компанией осуществляется отправка по россии?', callback_data='trans_comp'),
                InlineKeyboardButton(text='Как отследить заказ?', callback_data='track_order'),
                InlineKeyboardButton(text='🏠 На главную', callback_data='home'))
    builder.adjust(1)
    return builder.as_markup()


def ikb_come_quest():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text='🔙 К вопросам', callback_data='often_quest'))
    return builder.as_markup()


def ikb_where_link():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text='🔍 Где найти ссылку?', callback_data='where_link'),
                InlineKeyboardButton(text='🏠 На главную', callback_data='home'))
    return builder.as_markup()


def ikb_done():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text='📝 Изменить', callback_data='make_order'),
                InlineKeyboardButton(text='✅ Верно', callback_data='done_order'),
                InlineKeyboardButton(text='🏠 На главную', callback_data='home'))
    builder.adjust(1)
    return builder.as_markup()


def ikb_instruction():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text='📋 Регистрация аккаунта', callback_data='log_acc'),
                InlineKeyboardButton(text='📚 Гайд по приложению', callback_data='guide'),
                InlineKeyboardButton(text='🏠 На главную', callback_data='home'))
    builder.adjust(1)
    return builder.as_markup()


def ikb_come_instr():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text='🔙 Назад', callback_data='come_inst'))
    return builder.as_markup()


def ikb_sign(order_id):
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text='✅ Подтвердить', callback_data=f'id_{order_id}'))
    return builder.as_markup()


def ikb_admin():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text='🔄 Изменить курс', callback_data='change_cours'),
                InlineKeyboardButton(text='💳 Реквизиты', callback_data='change_pay'),
                InlineKeyboardButton(text='🏠 На главную', callback_data='home'))
    builder.adjust(1)
    return builder.as_markup()


def ikb_change_or_add():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text='📃 Добавить реквизиты', callback_data='add_propts'),
                InlineKeyboardButton(text='💳 Изменить отображаемые', callback_data='change_propts'))
    builder.adjust(1)
    return builder.as_markup()


def ikb_close_size():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text='❌ Нет размера', callback_data='close_size'),
                InlineKeyboardButton(text='🏠 На главную', callback_data='home'))
    builder.adjust(1)
    return builder.as_markup()


def ikb_propts():
    builder = InlineKeyboardBuilder()

    connect = sqlite3.connect('Poizon.db')
    cursor = connect.cursor()

    try:
        cursor.execute("SELECT id, bank, number, recipient FROM propts")
        rows = cursor.fetchall()

        for row in rows:
            acc_id, bank, number, recipient = row
            text = f"{bank} | {number} | {recipient}"  # Одной строкой, без переноса
            builder.row(
                InlineKeyboardButton(
                    text=text,
                    callback_data=f"select_acc_{acc_id}"
                )
            )
    except Exception as e:
        print("Ошибка при получении данных из БД:", e)
    finally:
        cursor.close()
        connect.close()

    return builder.as_markup()