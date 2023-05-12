import logging
import os

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text, state
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardRemove
from dotenv import load_dotenv

from api import get_letter, get_skills, add_skill
from buttons import letters
from constants import *
import utils

load_dotenv()

logging.basicConfig(level=logging.INFO)

bot = Bot(token=os.getenv('TELEGRAM_TOKEN'))
dp = Dispatcher(bot, storage=MemoryStorage())

message_stack = utils.MessageStack()


class LetterInput(state.StatesGroup):
    company = state.State()
    position = state.State()
    interest = state.State()
    requirements = state.State()


class SkillInput(state.StatesGroup):
    skill = state.State()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer(
        (
            f'Привет, {message.from_user.username}!!!\n'
            f'Список доступных комманд {COMMANDS_OFFER}\n'
        ),
        reply_markup=letters
    )


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
    bot_message = await message.answer(text=bot_answer)
    message_stack.push(bot_message.message_id)
    message_stack.push(message.message_id)
    await LetterInput.next()


async def start_letter(message: types.Message):
    """Вход в скрипт Написания письма."""
    bot_message = await message.answer(
        'Введите название компании', reply_markup=ReplyKeyboardRemove()
    )
    message_stack.push(bot_message.message_id)
    await LetterInput.company.set()


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
    """Принимает название компании."""
    await reciver(
        message, state,
        'company',
        'Введите позицию, на которую притендуете'
    )


@dp.message_handler(state=LetterInput.position)
async def position_reciver(message: types.Message, state: FSMContext):
    """Принимает желаемую позицию соискателя."""
    await reciver(
        message, state,
        'position',
        'К чему у вас интерес в этой компании?'
    )


@dp.message_handler(state=LetterInput.interest)
async def interest_reciver(message: types.Message, state: FSMContext):
    """Recive интерес and next step."""
    await reciver(message, state, 'interest', 'Добавте требования')


@dp.message_handler(state=LetterInput.requirements)
async def requirements_reciver_and_finish(message: types.Message,
                                          state: FSMContext):
    """Recive Требования вакансии description and_script_finish."""
    data = await state.get_data()
    data['requirements'] = message.text
    letter_data = await get_letter(data)
    await message.answer(f'Для компании {data["company"]}')
    await message.answer(text=letter_data.get('letter'))
    await state.finish()
    message_stack.push(message.message_id)
    await delete_messages(message)


@dp.message_handler(commands=['my_skills'])
async def get_user_skills(message: types.Message):
    """Дает все скиллы пользователя."""
    bot_answer = await get_skills(USER_SKILL_ENDPOINT)
    line_feed = '\n'
    bot_message = await message.answer(
        (
            '\tВаш стек:\n\n<code>'
            f'{line_feed.join(bot_answer["user_skills"])}</code>'
        ),
        parse_mode='HTML'
    )
    message_stack.push(bot_message.message_id)


@dp.message_handler(commands=['add_my_skill'])
async def add_user_skill(message: types.Message):
    """Интерфейс Добавления скилла в стэк пользователя."""
    await message.answer('Внесите ваш навык.')
    await SkillInput.skill.set()


@dp.message_handler(state=SkillInput.skill)
async def recive_user_skill(message: types.Message, state: FSMContext):
    """Принимает текст скилла, и отправляет на сервер, через API."""
    user_answer = {'text': message.text}
    server_answer = await add_skill(user_answer, USER_SKILL_ENDPOINT)
    await message.answer(server_answer['message'])
    await state.finish()


async def delete_messages(message: types.Message):
    """Удалить сообщения из стека сообщений."""
    while message_stack.length() != 0:
        message_id = message_stack.pop()
        await bot.delete_message(
            chat_id=message.chat.id, message_id=message_id
        )


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
