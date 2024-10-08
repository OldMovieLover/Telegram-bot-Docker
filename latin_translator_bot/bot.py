# 1.Импорт библиотек
import logging
import os

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery 
from aiogram.filters.command import Command, CommandStart 
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# 2. Инициализация объектов
TOKEN=os.getenv('TOKEN')
bot = Bot(token=TOKEN)
dp = Dispatcher()

# 3. Логирование в файл
logging.basicConfig(filename='bot.log', 
                    filemode='a',
                    level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S'
                    )

class Form(StatesGroup):
    waiting_for_text = State()

help_information = """/start - начало работы с ботом
/help - вызов меню команд
/info - информация о боте
/translit - выполнить транслитерацию текста"""

information = "Это телеграм-бот, который принимает в качестве сообщений текст в кириллице и отдаёт большими буквами на латинице в соответствии с Приказом МИД России от 12.02.2020 № 2113"

dictonari = {
    'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ё': 'E', 'Ж': 'ZH', 'З': 'Z', 
    'И': 'I', 'Й': 'I', 'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N', 'О': 'O', 'П': 'P', 'Р': 'R', 
    'С': 'S', 'Т': 'T', 'У': 'U', 'Ф': 'F', 'Х': 'KH', 'Ц': 'TS', 'Ч': 'CH', 'Ш': 'SH', 
    'Щ': 'SHCH', 'Ы': 'Y', 'Ь': '', 'Ъ': 'IE', 'Э': 'E', 'Ю': 'IU', 'Я': 'IA'
}

def translittera(t):
  return ''.join(dictonari.get(char, char) for char in t.upper())

# 4. Настройка кнопок
main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Транслитерация', callback_data='translittera')],
    [InlineKeyboardButton(text='Инфо', callback_data='inform')],
    [InlineKeyboardButton(text='Помощь', callback_data='helper')]
])

@dp.message(CommandStart())
async def proccess_command_start(message: Message):
    user_name = message.from_user.full_name
    user_id = message.from_user.id
    text = f"Привет, {user_name}!"
    logging.info(f"{user_name} {user_id} запустил бота")
    await bot.send_message(chat_id=user_id, text=text, reply_markup=main)

# 5. Обработка вызова транслитерации по кнопке/команде
@dp.callback_query(F.data == 'translittera')
async def process_callback_translit(callback: CallbackQuery, state: FSMContext):
    user_name = callback.from_user.full_name
    user_id = callback.from_user.id
    logging.info(f"{user_name} {user_id} нажал на кнопку 'Транслитерация'")
    await callback.answer()
    await state.set_state(Form.waiting_for_text)    
    await bot.send_message(callback.from_user.id, "Введите текст для трнаслитерации")

@dp.message(Command('translit'))
async def process_translit_command(message: Message, state: FSMContext):
    user_name = message.from_user.full_name
    user_id = message.from_user.id
    logging.info(f"{user_name} {user_id} по команде обратился в 'Транслитерация'")
    await message.answer("Введите текст для трнаслитерации")
    await state.set_state(Form.waiting_for_text)  

# 6. Обработка вызова информации по кнопке/команде
@dp.callback_query(F.data == 'inform')
async def process_callback_info(callback: CallbackQuery):
    user_name = callback.from_user.full_name
    user_id = callback.from_user.id
    logging.info(f"{user_name} {user_id} нажал на кнопку 'Инфо'")
    await callback.answer()
    await callback.message.answer(text=information, reply_markup=main)

@dp.message(Command('info'))
async def process_info_command(message: Message):
    user_name = message.from_user.full_name
    user_id = message.from_user.id
    logging.info(f"{user_name} {user_id} по команде обратился в 'Инфо'")
    await bot.send_message(chat_id=message.chat.id, text=information, reply_markup=main) 

# 7. Обработка вызова помощи по кнопке/команде
@dp.callback_query(F.data == 'helper')
async def process_callback_help(callback: CallbackQuery):
    user_name = callback.from_user.full_name
    user_id = callback.from_user.id
    logging.info(f"{user_name} {user_id} нажал на кнопку 'Помощь'")
    await callback.answer()
    await callback.message.answer(text=help_information, reply_markup=main)

@dp.message(Command('help'))
async def process_info_command(message: Message):
    user_name = message.from_user.full_name
    user_id = message.from_user.id
    logging.info(f"{user_name} {user_id} по команде обратился в 'Помощь'")
    await bot.send_message(chat_id=message.chat.id, text=help_information, reply_markup=main) 

# 8. Отработка сообщения зарегистрированного для транслитерации
@dp.message(Form.waiting_for_text)
async def tranlit(message: Message, state: FSMContext):
    text = translittera(message.text)
    user_name = message.from_user.full_name
    user_id = message.from_user.id
    logging.info(f"{user_name} {user_id}: {message.text}")
    await message.reply(text=text, reply_markup=main)
    await state.set_state()
 
# 9. Обработка всех сообщений    
@dp.message()
async def proccess_command_start(message: Message):
    user_name = message.from_user.full_name
    user_id = message.from_user.id
    text = "Для начала работы с ботом используйте /start или воспользуйтесь комнадой /help"
    logging.info(f"{user_name} {user_id}: {message.text}")
    await message.answer(text=text)

# 10. Запуск процесса пуллинга
if __name__ == '__main__':
    dp.run_polling(bot)