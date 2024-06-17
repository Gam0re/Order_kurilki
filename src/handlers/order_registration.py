from aiogram import Router, types, F

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

from src.bot import bot
import src.database.requests as rq

from src.database.models import Order, async_session

from src.data.config import MANAGER_ID


order_registration_router = Router()



@order_registration_router.callback_query(F.data == 'continue')
async def sending_order(callback: types.CallbackQuery, widget: Button, dialog_manager: DialogManager):
    try:
        await dialog_manager.done()
    except:
        pass
    await callback.message.delete()
    products = [(await rq.get_product(order.prod_id), order.amount) for order in
                                      await rq.orm_get_user_carts(callback.from_user.id)]
    product_strings = [f"{product[0].brand} {product[0].puffs} {product[0].flavor} кол-во: {product[1]} шт." for product in products]
    await bot.send_message(MANAGER_ID,
                           f"Новый заказ от пользователя @{callback.from_user.username} на имя: {await rq.get_name(callback.from_user.id)}\nНомер телефона: {await rq.get_number(callback.from_user.id)}\n" +
                           "\n".join([string for string in product_strings]),)
    await callback.message.answer("Ваш заказ успешно оформлен! 🔥\nСпасибо, что выбрали HotSmok🙌 Наш менеджер свяжется с Вами в течение 24 часов!")
    await rq.orm_update_status(callback.from_user.id, 'shop', 'in_progress')


