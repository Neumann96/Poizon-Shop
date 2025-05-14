from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import FSInputFile
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

start_message = '''
😉 <b>Добро пожаловать в бот группы <u>logistic by pumba</u>!</b>

🛍 Мы помогаем <b>выкупать товары исключительно с китайской площадки <u>POIZON (DEWU)</u></b>.

⛔️ <b>Все расчёты, заказы и оплата производятся <u>только в этом боте</u>.</b>  
<i>Оплата в личных сообщениях — не принимается!</i>

⚠️ <b>Возврату и обмену товар <u>не подлежит</u>.</b>  
<i>Мы оказываем только услуги выкупа и доставки.</i>
'''

name = ''


class Client(StatesGroup):
    calc_price = State()
    cours = State()


@dp.message(Command("start"), StateFilter(None))
async def start_command(message: Message, state: FSMContext):
    photo = FSInputFile("pumba_pic.jpg")
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
    photo = FSInputFile("pumba_pic.jpg")
    await bot.send_photo(chat_id=callback.message.chat.id,
                         photo=photo,
                         caption=f'{start_message}',
                         parse_mode='HTML',
                         reply_markup=get_ikb_start())


@dp.callback_query(F.data == 'make_order')
async def quest(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer('А здесь сделаем оформление заказа!',
                                  reply_markup=ikb_come_home())


@dp.callback_query(F.data == 'often_quest')
async def quest(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer('❓Есть вопросы? Возможно, ответ уже ждёт вас здесь.',
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
                                    text='📊 В нашем калькуляторе Вы можете сделать расчет стоимости товара с доставкой до России.\n\n'
                                         '💬 Выберите подходящий раздел:',
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
        res = price * cours + 1000 + comission
        await message.bot.send_message(chat_id=message.from_user.id,
                                       text=f'💰 Итоговая стоимость товара <b>{res} рублей</b>\n\n'
                                            f'Комиссия сервиса: <b>1000 рублей</b> (уже включена в итоговую стоимость)\n\n'
                                            f'Доставка на выбранный тип товара: <b>{comission} рублей</b>\n\n'
                                            f'📊 Курс юаня: <b>{cours}</b>',
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


if __name__ == '__main__':
    print('Work Work')
    dp.run_polling(bot, skip_updates=True)