from aiogram.fsm.state import State, StatesGroup


class UserFSM(StatesGroup):
    settings_menu = State()
    write_message = State()
    write_name = State()
    write_phone = State()
    rewrite_name = State()
    rewrite_phone = State()
