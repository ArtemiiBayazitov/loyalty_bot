from aiogram.fsm.state import State, StatesGroup


class Register(StatesGroup):
    phone_number = State()
    last_name = State()
    first_name = State()
    email = State()
    date_of_birth = State()
    sex = State()


