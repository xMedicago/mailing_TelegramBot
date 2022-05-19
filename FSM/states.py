from aiogram.dispatcher.filters.state import StatesGroup, State


class Spam(StatesGroup):
    text = State()
    users = State()
    confirmation = State()
