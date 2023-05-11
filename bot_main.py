import logging
import os

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text, state
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardRemove
from dotenv import load_dotenv

from constants import *
from api import get_letter2, recognize_req
from buttons import letters
# from buttons import calendar

load_dotenv()

logging.basicConfig(level=logging.INFO)

bot = Bot(token=os.getenv('TELEGRAM_TOKEN'))
dp = Dispatcher(bot, storage=MemoryStorage())


class LetterInput(state.StatesGroup):
    company = state.State()
    position = state.State()
    interest = state.State()
    requirements = state.State()

class Requirements(state.StatesGroup):
    requirements = state.State()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer(
        (
        f'Привет, {message.from_user.username}!!!\n'
        f'Список доступных комманд {COMMANDS_OFFER}\n'
        ),
        reply_markup=letters
    )

# +++
async def reciver(message: types.Message,
                  state: FSMContext,
                  key: str,
                  bot_answer: str):
    """
    Common function for reciving data and save data to StateGroup.
    Also invites you to take the next step.
    """
    data = {key: message.text}
    await state.update_data(data=data)
    await message.answer(text=bot_answer)
    await LetterInput.next()


async def start_letter(message: types.Message):
    await message.answer(
        'Введите название компании', reply_markup=ReplyKeyboardRemove()
    )
    await LetterInput.company.set()


@dp.message_handler(commands=['recognize'])
async def recognize_requirements(message: types.Message):
    await message.answer('Внесите текст зависимостей.')
    await Requirements.requirements.set()

@dp.message_handler(state=Requirements.requirements)
async def requirements_reciver(message: types.Message,
                               state: FSMContext):
    answer = message.text
    response = await recognize_req({'text': answer})
    result = ''
    for line in response['filtered_data']:
        result += f'{line}\n'
    await message.answer(result)
    await state.finish()


@dp.message_handler(commands=['letter'])
async def start_letter_writing_with_command(message: types.Message,
                                            state: FSMContext):
    """Stars script letter_writing with command."""
    await start_letter(message)


@dp.message_handler(Text('Письмо'))
async def start_letter_writing_with_button(message: types.Message,
                                           state: FSMContext):
    """Stars script letter_writing with button."""
    await start_letter(message)


@dp.message_handler(state=LetterInput.company)
async def company_reciver(message: types.Message, state: FSMContext):
    """Нет."""
    await reciver(
        message, state,
        'company',
        'Введите позицию, на которую притендуете'
    )


@dp.message_handler(state=LetterInput.position)
async def position_reciver(message: types.Message, state: FSMContext):
    """Нет."""
    await reciver(
        message, state,
        'position',
        'К чему у вас интерес в этой компании?'
    )


@dp.message_handler(state=LetterInput.interest)
async def interest_reciver(message: types.Message, state: FSMContext):
    """Recive event time and next step."""
    await reciver(message, state, 'interest', 'Добавте требования')

# @dp.message_handler(state=LetterInput.requirements)
# async def requirements_reciver_and_finish(message: types.Message, state: FSMContext):
#     """Recive event description and_script_finish."""
#     start = datetime.datetime.now()
#     print(start)
#     requirements = await get_skills({'text': message.text})
#     data = await state.get_data()
#     data['requirements'] = requirements['filtered_data']
#     letter_data = await get_letter(data)
#     await message.answer(text=letter_data.get('letter'))
#     stop = datetime.datetime.now()
#     print(stop)
#     await message.answer(text=stop-start)
#     await state.finish()

@dp.message_handler(state=LetterInput.requirements)
async def requirements_reciver_and_finish(message: types.Message,
                                          state: FSMContext):
    """Recive event description and_script_finish."""
    data = await state.get_data()
    data['requirements'] = message.text
    letter_data = await get_letter2(data)
    await message.answer('fuck')
    await message.answer(text=letter_data.get('letter'))
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)