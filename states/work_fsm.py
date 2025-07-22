from aiogram.fsm.state import State, StatesGroup


class WorkState(StatesGroup):
    # start = State()
    lesson = State()
    company = State()
    description = State()
    offer = State()
    contact = State()


