from aiogram import types, Router, F

from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

from aiogram_dialog import DialogManager

import src.database.requests as rq
import src.keyboards.default.reply as kb

account_router = Router()


@account_router.message(F.text == 'Личный кабинет')
async def to_personal_account(message: types.Message, state: FSMContext, dialog_manager: DialogManager):
    try:
        await dialog_manager.done()
    except:
        pass
    await message.answer("Вы перешли в личный кабинет.\nВыберете необходимую опцию", reply_markup=kb.account_kb)


@account_router.message(F.text == 'История заказов')
async def to_personal_account(message: types.Message):
    orders = await rq.get_orders(message.from_user.id)
    if orders:
        await message.answer("Вы заказывали:\n" + "\n".join([" ".join(await rq.get_products(order[0].prod_id)) + f" в количестве: {order[0].amount}" for order in orders]),
                             reply_markup=kb.account_kb)
    else:
        await message.answer("Вы ещё ничего у нас не заказывали", reply_markup=kb.account_kb)
