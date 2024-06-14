from aiogram import types, Router, F

from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
import src.keyboards.default.reply as kb

import src.database.requests as rq
import src.states.user as user_states

registration_router = Router()


async def start_registration_name(message: types.Message, state: FSMContext):
    await message.answer('Отлично!\nВы у нас первый раз?\nДавайте заполним некоторые данные\nВведите своё ФИО:')
    await state.set_state(user_states.UserFSM.write_name)


@registration_router.message(StateFilter(user_states.UserFSM.write_name))
async def registration_name(message: types.Message, state: FSMContext):
    await state.update_data(user_name=message.text)
    await message.answer('Отправьте свой номер телефона', reply_markup=kb.send_contact_kb)
    await state.set_state(user_states.UserFSM.write_phone)


@registration_router.message(StateFilter(user_states.UserFSM.write_phone), F.content_type == 'contact')
async def registration_phone(message: types.Message, state: FSMContext):
    await state.update_data(user_phone=message.contact.phone_number)
    user_data = await state.get_data()
    await rq.update_name_phone(message.from_user.id, name=user_data.get('user_name'),
                               phone=user_data.get('user_phone'))
    await message.answer('Регистрация прошла успешно!', reply_markup=kb.start_kb)
    await state.set_state(default_state)
