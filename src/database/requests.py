from src.utils.funcs import get_image_ratio, get_image_size
from src.database.models import async_session, User, Catalog, Order
from sqlalchemy import select, delete


async def set_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()


async def check_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            return False
        else:
            return True


async def update_name_phone(tg_id, **kwargs):
    async with async_session() as session:
        user_id = await session.scalar(select(User.id).where(User.tg_id == tg_id))
        user = await session.get(User, user_id)
        for data_type, data in kwargs.items():
            if data_type == 'name':
                user.name = data
            if data_type == 'phone':
                user.phone = data
            await session.commit()


async def get_name(tg_id):
    async with async_session() as session:
        name = await session.scalar(select(User.name).where(User.tg_id == tg_id))
        return name


async def get_number(tg_id):
    async with async_session() as session:
        phone = await session.scalar(select(User.phone).where(User.tg_id == tg_id))
        return phone


async def get_orders(tg_id):
    async with async_session() as session:
        query = select(Order).where(Order.tg_id == tg_id, Order.status == 'in_progress')
        result = await session.execute(query)
        return result.all()


async def write_to_order(tg_id, product, quant):
    async with async_session() as session:
        session.add(Order(tg_id=tg_id, prod_id=product, amount=quant))
        await session.commit()

async def get_products(prod_id):
    async with async_session() as session:
        query = select(Catalog.brand, Catalog.puffs, Catalog.flavor).where(Catalog.id == prod_id)
        result = await session.execute(query)
        return result.first()

async def orm_add_to_cart(tg_id: int, prod_id: int, quant: int):
    async with async_session() as session:
        query = select(Order).where(Order.tg_id == tg_id, Order.prod_id == prod_id)
        cart = await session.execute(query)
        cart = cart.scalar()
        if cart:
            cart.amount += quant
            await session.commit()
            return cart
        else:
            session.add(Order(tg_id=tg_id, prod_id=prod_id, amount=quant, status='shop'))

            await session.commit()

async def get_order_price(tg_id):
    data = await orm_get_user_carts(tg_id)
    order_price = 0
    for order in data:
        order_price += float((await get_product(order.prod_id)).price) * int(order.amount)
    return order_price

async def get_product(prod_id):
    async with async_session() as session:
        query = select(Catalog).where(Catalog.id == prod_id)
        result = await session.execute(query)
        return result.scalar()

async def get_amount(order):
    async with async_session() as session:
        return await session.scalar(select(order.amount))
async def orm_get_user_carts(tg_id):
    async with async_session() as session:
        query = select(Order).where(Order.tg_id == tg_id, Order.status == 'shop')
        result = await session.execute(query)
        return result.scalars().all()

async def orm_delete_from_cart(tg_id: int, product_id: int):
    async with async_session() as session:
        query = delete(Order).where(Order.tg_id == tg_id, Order.prod_id == product_id, Order.status == 'shop')
        await session.execute(query)
        await session.commit()

async def orm_reduce_product_in_cart(tg_id: int, product_id: int):
    async with async_session() as session:
        query = select(Order).where(Order.tg_id == tg_id, Order.prod_id == product_id, Order.status == 'shop')
        cart = await session.execute(query)
        cart = cart.scalar()

        if not cart:
            return
        if cart.amount > 1:
            cart.amount -= 1
            await session.commit()
            return True
        else:
            await orm_delete_from_cart(tg_id, product_id)
            await session.commit()
            return False

async def orm_update_status(tg_id, from_status, to_status):
    async with async_session() as session:
        query = select(Order).where(Order.tg_id == tg_id, Order.status == from_status)
        carts = await session.execute(query)
        carts = carts.scalars()

        for cart in carts:
            cart.status = to_status
        await session.commit()

