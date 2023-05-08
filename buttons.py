from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData


# letter  = KeyboardButton(text='Письмо')
letter = KeyboardButton('Письмо')
# buttons = InlineKeyboardMarkup()

letters = ReplyKeyboardMarkup(resize_keyboard=True)
letters.add(letter)
