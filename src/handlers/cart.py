from aiogram import types, Router, F

from aiogram.filters import Command

from aiogram_dialog import DialogManager, StartMode
from src.dialogs.Cart.states import Cart_levels
import src.database.requests as rq
import src.keyboards.default.reply as kb

cart_router = Router()


# корзина
@cart_router.message(Command('cart'))
@cart_router.message(F.text == 'Корзина')
async def get_carts(message: types.Message, dialog_manager: DialogManager):
    try:
        await dialog_manager.done()
    except:
        pass
    if await rq.orm_get_user_carts(message.from_user.id) == []:
        await message.answer('Корзина пуста', reply_markup=kb.start_kb)
    else:
        await dialog_manager.start(Cart_levels.select_products, data={'user_id': message.from_user.id}, mode=StartMode.RESET_STACK)

@cart_router.callback_query(F.data == 'go_to_cart')
@cart_router.callback_query(F.data == 'disagree')
async def get_carts_call(callback: types.CallbackQuery, dialog_manager: DialogManager):
    try:
        await dialog_manager.done()
    except:
        pass
    if await rq.orm_get_user_carts(callback.from_user.id) == []:
        await callback.answer('Корзина пуста', reply_markup=kb.start_kb)
    else:
        await dialog_manager.start(Cart_levels.select_products, data={'user_id': callback.from_user.id}, mode=StartMode.RESET_STACK)
