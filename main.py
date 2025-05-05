from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import FSInputFile

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


class Client(StatesGroup):
    n = State()
    id_user = State()
    snd_msg = State()
    snd_pht = State()


@dp.message(Command("start"), StateFilter(None))
async def start_command(message: Message, state: FSMContext):
    photo = FSInputFile("pumba_pic.jpg")
    try:
        await bot.send_photo(chat_id=message.chat.id,
                             photo=photo,
                             caption=f'{start_message}',
                             parse_mode='HTML')
    except Exception as e:
        print(f'Ошибка при /start: {e.__class__.__name__}: {e}')


if __name__ == '__main__':
    print('Work Work')
    dp.run_polling(bot, skip_updates=True)