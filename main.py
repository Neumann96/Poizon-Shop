from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import FSInputFile
from texts import *
import re

from keyboards import *
from sql_query import *
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv('token_test')
proxy_url = os.getenv('proxy_url')

storage = MemoryStorage()
bot = Bot(token=token, proxy=proxy_url)
dp = Dispatcher(storage=storage)

name = ''


class Client(StatesGroup):
    calc_price = State()
    cours = State()
    order_kat = State()
    picture = State()
    link = State()
    size = State()
    price = State()
    result = State()
    done = State()
    mail = State()


@dp.message(Command("start"), StateFilter('*'))
async def start_command(message: Message, state: FSMContext):
    photo = FSInputFile("media/pumba_pic.jpg")
    await state.clear()
    try:
        await bot.send_photo(chat_id=message.chat.id,
                             photo=photo,
                             caption=f'{start_message}',
                             parse_mode='HTML',
                             reply_markup=get_ikb_start())
    except Exception as e:
        print(f'Ошибка при /start: {e.__class__.__name__}: {e}')


@dp.callback_query(StateFilter('*'), F.data == 'home')
async def calc_price(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.clear()
    photo = FSInputFile("media/pumba_pic.jpg")
    await bot.send_photo(chat_id=callback.message.chat.id,
                         photo=photo,
                         caption=f'{start_message}',
                         parse_mode='HTML',
                         reply_markup=get_ikb_start())


@dp.callback_query(F.data == 'make_order')
async def quest(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(calc_text,
                                  reply_markup=get_ikb_kat())
    await state.set_state(Client.order_kat)


@dp.callback_query(F.data == 'instructions')
async def quest(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer('Выберите раздел:',
                                  reply_markup=ikb_instruction())


@dp.callback_query(F.data == 'log_acc')
async def quest(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    file1 = FSInputFile('media/log_acc_1.jpg')
    file2 = FSInputFile('media/log_acc_2.jpg')
    file3 = FSInputFile('media/log_acc_3.jpg')
    file4 = FSInputFile('media/log_acc_4.jpg')
    photos = [
        InputMediaPhoto(media=file1, caption=log_acc_text, parse_mode='HTML'),
        InputMediaPhoto(media=file2),
        InputMediaPhoto(media=file3),
        InputMediaPhoto(media=file4)
    ]
    await bot.send_media_group(chat_id=callback.message.chat.id,
                               media=photos)
    await callback.message.answer('Выберите раздел:',
                                  reply_markup=ikb_instruction())


@dp.callback_query(F.data == 'guide')
async def quest(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    file1 = FSInputFile('media/guide_1.jpg')
    file2 = FSInputFile('media/guide_2.jpg')
    file3 = FSInputFile('media/guide_3.jpg')
    file4 = FSInputFile('media/guide_4.jpg')
    file5 = FSInputFile('media/guide_5.jpg')
    photos = [
        InputMediaPhoto(media=file1, caption=guide_text, parse_mode='HTML'),
        InputMediaPhoto(media=file2),
        InputMediaPhoto(media=file3),
        InputMediaPhoto(media=file4),
        InputMediaPhoto(media=file5)
    ]
    await bot.send_media_group(chat_id=callback.message.chat.id,
                               media=photos)
    await callback.message.answer('Выберите раздел:',
                                  reply_markup=ikb_instruction())


@dp.callback_query(lambda c: c.data.startswith("calc_"), StateFilter(Client.order_kat))
async def order_kat(callback: CallbackQuery, state: FSMContext):
    photo = FSInputFile("media/example.PNG")
    await state.update_data(kat=callback.data[5:])
    await callback.message.delete()
    await callback.bot.send_photo(chat_id=callback.message.chat.id,
                                  photo=photo,
                                  caption=f'🖼️ Пожалуйста, вставьте скриншот страницы товара, как показано на примере',
                                  parse_mode='HTML')
    await callback.answer()
    await state.set_state(Client.picture)


@dp.message(StateFilter(Client.picture))
async def picture(message: Message, state: FSMContext):
    if not message.photo:
        await message.answer("Пожалуйста, отправьте фотографию.",)
        return
    photo = message.photo[-1]
    file_id = photo.file_id
    await state.update_data(photo_id=file_id)
    await message.answer(text="<b>🔗 Пожалуйста, отправьте ссылку на товар</b>",
                         reply_markup=ikb_where_link(),
                         parse_mode="HTML")
    await state.set_state(Client.link)


@dp.message(StateFilter(Client.link))
async def link(message: Message, state: FSMContext):
    if 'https://dw4.co' in message.text:
        match = re.search(r'https?://\S+', message.text)
        await state.update_data(link=match.group())
        await message.answer(text='📏 Пожалуйста, напишите размер товара (актуально для одежды и обуви).\n\n'
                             'Например: 42',
                             parse_mode='HTML')
        await state.set_state(Client.size)
    else:
        await message.answer('Это не ссылка, отправьте пожалйуста ссылку!')


@dp.message(StateFilter(Client.size))
async def size(message: Message, state: FSMContext):
    if message.text.isdigit() or '.' in message.text or ',' in message.text:
        await state.update_data(size=message.text)
        await message.answer(text='❕Введите стоимость выбранной вами позиции в Юанях:',
                             parse_mode='HTML')
        await state.set_state(Client.price)
    else:
        await message.answer('Введите, пожалуйста, размер!')


@dp.message(StateFilter(Client.price))
async def price(message: Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(price=message.text)
        data = await state.get_data()
        price = int(data.get('price'))
        cours = get_cours()[0]
        comission = get_price_comission(data.get('kat'))[0]
        res = int(price * cours + 1000 + comission)
        await bot.send_photo(chat_id=message.chat.id,
                             caption=f'🔗 Ссылка на товар: {data.get("link")}\n'
                                     f'🧩 Размер: {data.get("size")}\n'
                                     f'💴 Стоимость товара в Юанях: {data.get("price")}¥\n'
                                     f'💳 Итоговая стоимость заказа: {res}₽\n\n'
                                     f'Проверьте, пожалуйста, правильность введенных вами данных!',
                             photo=data.get('photo_id'),
                             parse_mode='HTML',
                             reply_markup=ikb_done()
                             )
        await state.set_state(Client.done)
    else:
        await message.answer('Введите, пожалуйста, стоимость!')


@dp.callback_query(StateFilter(Client.done))
async def result(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer(mail_text)
    await state.set_state(Client.mail)


@dp.message(StateFilter(Client.mail))
async def result(message: Message, state: FSMContext):
    if message.text.count('\n') >= 6:
        await message.answer(f'<b>✅ Заказ принят!</b>\n\n'
                             f'Ожидайте подтверждения, для совершения оплаты!',
                             parse_mode='HTML')
        data = await state.get_data()
        price = int(data.get('price'))
        cours = get_cours()[0]
        comission = get_price_comission(data.get('kat'))[0]
        res = int(price * cours + 1000 + comission)
        order_id = await add_order(message.from_user.id)
        await bot.send_photo(chat_id=1006103801,
                       caption=f'🔗 Ссылка на товар: {data.get("link")}\n'
                               f'🧩 Размер: {data.get("size")}\n'
                               f'💴 Стоимость товара в Юанях: {data.get("price")}¥\n'
                               f'💳 Итоговая стоимость заказа: {res}₽\n'
                               f'Курс: {cours}\n\n'
                               f'Информация по доставке:\n'
                               f'{message.text}',
                       photo=data.get('photo_id'),
                       reply_markup=ikb_sign(order_id),
                       parse_mode='HTML')
    else:
        await message.answer('Ваше сообщение не соответствует нужному формату')
    await state.clear()


@dp.callback_query(lambda c: c.data.startswith("id_"))
async def order_kat(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer(callback.data)


@dp.callback_query(F.data == 'often_quest')
async def quest(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer('❓ Есть вопросы? Возможно, ответ уже ждёт вас здесь.',
                                  reply_markup=ikb_often_question())


@dp.callback_query(F.data == 'time_delivery')
async def quest(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer('Доставка занимает от 3 до 5 недель с момента прибытия товара '
                                  'на склад в Китае. Срок может незначительно варьироваться в зависимости от вашего города.',
                                  reply_markup=ikb_come_quest())


@dp.callback_query(F.data == 'trans_comp')
async def quest(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer('По России все заказы доставляются через Почту России.',
                                  reply_markup=ikb_come_quest())


@dp.callback_query(F.data == 'track_order')
async def quest(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer('Как только посылка будет передана в доставку по '
                                  'России, вы получите SMS-уведомление с информацией для отслеживания.',
                                  reply_markup=ikb_come_quest())


@dp.callback_query(F.data == 'calc')
async def calc_price(callback: CallbackQuery):
    await callback.message.delete()
    await callback.bot.send_message(chat_id=callback.from_user.id,
                                    text=calc_text,
                                    reply_markup=get_ikb_kat())
    await callback.answer()


@dp.callback_query(lambda c: c.data.startswith("calc_"))
async def res_calc(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    global name
    name = callback.data
    await callback.bot.send_message(chat_id=callback.from_user.id,
                                    text='Напишите стоимость товара в юанях:')
    await state.set_state(Client.calc_price)


@dp.message(StateFilter(Client.calc_price))
async def res_calc2(message: Message, state: FSMContext):
    global name
    if message.text.isdigit():
        price = int(message.text)
        cours = get_cours()[0]
        comission = get_price_comission(name[5:])[0]
        res = int(price * cours + 1000 + comission)
        await message.bot.send_message(chat_id=message.from_user.id,
                                       text=f'💳 Итоговая стоимость заказа: <b>{res} рублей</b>\n\n'
                                            f'🚚 Стоимость доставки: <b>{comission} рублей</b>\n'
                                            f'💸 Комиссия: <b>1000₽</b>\n'
                                            f'📊 Курс: <b>{cours}</b>',
                                       parse_mode='HTML',
                                       reply_markup=ikb_home_order())
        await state.clear()
    else:
        await message.answer('Вы ввели не стоимость, попробуйте ещё раз!')


@dp.message(Command('admin'))
async def admin(message: Message, state: FSMContext):
    if message.from_user.username == 'nmnn96' or message.from_user.username == 'lottematte':
        await message.answer('Напиши новый курс юаня вещественным числом через точку:')
        await state.set_state(Client.cours)
    else:
        return


@dp.message(StateFilter(Client.cours))
async def admin(message: Message, state: FSMContext):
    try:
        n = float(message.text)
        if not n.is_integer():
            change_cours(n)
            await message.answer(f'Курс успешно изменён!\n\n'
                                 f'Новый курс: {get_cours()[0]}')
            await state.clear()
        else:
            await message.answer('Вы ввели не вещественное число')
    except ValueError:
        await message.answer('Вы ввели не вещественное число')


@dp.callback_query(F.data == 'where_link')
async def where_link(callback: CallbackQuery):
    await callback.answer()
    file1 = FSInputFile('media/link_1.jpg')
    file2 = FSInputFile('media/link_2.jpg')
    photos = [
        InputMediaPhoto(media=file1, caption=where_link_text, parse_mode='HTML'),
        InputMediaPhoto(media=file2)
    ]
    await bot.send_media_group(chat_id=callback.message.chat.id,
                               media=photos)


if __name__ == '__main__':
    print('Work Work')
    dp.run_polling(bot, skip_updates=True)