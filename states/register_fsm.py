from aiogram.fsm.state import State, StatesGroup


class Register(StatesGroup):
    start = State()
    phone_number = State()
    last_name = State()
    first_name = State()
    email = State()
    date_of_birth = State()
    sex = State()
    check_data = State()
    save_data = State


class MainMenu(StatesGroup):
    main_menu = State()
