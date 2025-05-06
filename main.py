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

from scripts.regsetup import description

proxy_url = 'http://proxy.server:3128'
storage = MemoryStorage()
bot = Bot(token='7690649283:AAEHAtp1I73ksF14zzO9IBHdeBYl3Do_hrU', proxy=proxy_url)
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
    price = int(message.text)
    cours = 11.6
    comission = get_price_comission(name[5:])[0]
    print(comission)
    res = price * cours + 1000 + comission
    await message.bot.send_message(chat_id=message.from_user.id,
                                   text=f'💰 Итоговая стоимость товара <b>{res} рублей</b>\n'
                                         f'Комиссия сервиса: <b>1000 рублей</b> (уже включена в итоговую стоимость)\n\n'
                                         f'📊 Курс юаня: <b>{cours}</b>',
                                    parse_mode='HTML')
    await state.clear()


if __name__ == '__main__':
    print('Work Work')
    dp.run_polling(bot, skip_updates=True)