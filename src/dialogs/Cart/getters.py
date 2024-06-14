from src.database.models import async_session, Order, Catalog
from sqlalchemy import select
from src.utils.funcs import get_image_size, get_image_ratio
from src.database.requests import get_order_price
from aiogram_dialog import DialogManager



#получение товаров в корзине
async def get_products(dialog_manager: DialogManager, **middleware_data):
     async with async_session() as session:
        db_main = set(await session.scalars(select(Order.prod_id).where(Order.tg_id == dialog_manager.current_context().start_data.get('user_id'), Order.status == 'shop')))
        products = [(item, await session.scalar(select(Catalog).where(Catalog.id == item))) for item in db_main]
        data = {
            'products': [(item, f"{product.brand} {product.puffs} {product.flavor}") for item, product in products],
        }
        return data


async def get_item(dialog_manager: DialogManager, **middleware_data):
    async with async_session() as session:
        db_main = await session.scalar(
            select(Catalog).where(Catalog.id == int(dialog_manager.current_context().dialog_data.get('product_id'))))
        db_quantity = await session.scalar(select(Order.amount).where(Order.prod_id == int(dialog_manager.current_context().dialog_data.get('product_id'))))

        data = {'brand': db_main.brand,
                'image': db_main.image,
                'flavor': db_main.flavor,
                'puffs': db_main.puffs,
                'volume': db_main.volume,
                'nicotine': db_main.nicotine,
                'heat_element': db_main.heat_element,
                'battery': db_main.battery,
                'connector': db_main.connector,
                'compound': db_main.compound
                }

        return data

