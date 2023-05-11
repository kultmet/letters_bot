from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


letter = KeyboardButton('Письмо')

letters = ReplyKeyboardMarkup(resize_keyboard=True)
letters.add(letter)
