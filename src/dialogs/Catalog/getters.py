from src.database.models import async_session, Catalog
# lvl2_base, lvl3_base, lvl4_base, lvl5_base
from sqlalchemy import select
from src.utils.funcs import get_image_size, get_image_ratio
from .states import Catalog_levels
from aiogram_dialog import DialogManager


order = ['SeaBear', 'Air Stick', 'EPE', 'Puff']


#получение значений для 3 уровня
async def get_level_3(dialog_manager: DialogManager, **middleware_data):
     async with async_session() as session:
        db_main = list(set(await session.scalars(select(Catalog.brand))))
        item_ids = [db_main.index(i) for i in order]
        db_main = [db_main[i] for i in item_ids]
        db_main_items = set(await session.scalars(select(Catalog)))
        data = {'lvl3': [(brand, await session.scalar(select(Catalog.id).where(Catalog.brand == brand))) for brand in db_main],
                'lvl3_item': [(item.brand, item.id) for item in db_main_items]}
        return data


#получение значений для 4 уровня
async def get_level_4(dialog_manager: DialogManager, **middleware_data):
     async with async_session() as session:
        lvl3_name = await session.scalar(select(Catalog.brand).where(Catalog.id == int(dialog_manager.current_context().dialog_data.get('level_3'))))
        db_main = set(await session.scalars(select(Catalog.puffs).where(Catalog.brand == lvl3_name)))
        db_main_items = set(await session.scalars(select(Catalog).where(Catalog.brand == lvl3_name)))
        data = {'lvl4': [(puffs, await session.scalar(select(Catalog.id).where(Catalog.puffs == puffs, Catalog.brand == lvl3_name))) for puffs in db_main],
                'lvl4_item': [(item.puffs, item.id) for item in db_main_items]}
        return data

#получение значений для 5 уровня
async def get_level_5(dialog_manager: DialogManager, **middleware_data):
     async with async_session() as session:
        lvl3_name = await session.scalar(select(Catalog.brand).where(Catalog.id == int(dialog_manager.current_context().dialog_data.get('level_3'))))
        lvl4_name = await session.scalar(select(Catalog.puffs).where(Catalog.id == int(dialog_manager.current_context().dialog_data.get('level_4'))))
        db_main = set(await session.scalars(select(Catalog.flavor).where(Catalog.brand == lvl3_name, Catalog.puffs == lvl4_name)))
        data = {'lvl5': [(flavor, await session.scalar(select(Catalog.id).where(Catalog.flavor == flavor, Catalog.brand == lvl3_name))) for flavor in db_main]}
        return data

#получение значений товаров
async def get_selected_items(dialog_manager: DialogManager, **middleware_data):
     async with async_session() as session:
        level = dialog_manager.current_context().dialog_data.get('select_items')
        if level == 'level_5':
            lvl2_name = await session.scalar(select(lvl2_base.level_2).where(lvl2_base.id == int(dialog_manager.current_context().dialog_data.get('level_2'))))
            lvl3_name = await session.scalar(select(lvl3_base.level_3).where(lvl3_base.id == int(dialog_manager.current_context().dialog_data.get('level_3'))))
            lvl4_name = await session.scalar(select(lvl4_base.level_4).where(lvl4_base.id == int(dialog_manager.current_context().dialog_data.get('level_4'))))
            db_main_items = set(await session.scalars(select(Catalog).where(Catalog.level_5 == '', Catalog.level_4 == lvl4_name, Catalog.level_3 == lvl3_name, Catalog.level_2 == lvl2_name)))
            data = {'item': [(f'{item.name.split()[-1]} ({item.price} Руб.)', item.id) for item in db_main_items]}
            return data
        else:
            lvl2_name = await session.scalar(select(lvl2_base.level_2).where(lvl2_base.id == int(dialog_manager.current_context().dialog_data.get('level_2'))))
            lvl3_name = await session.scalar(select(lvl3_base.level_3).where(lvl3_base.id == int(dialog_manager.current_context().dialog_data.get('level_3'))))
            lvl4_name = await session.scalar(select(lvl4_base.level_4).where(lvl4_base.id == int(dialog_manager.current_context().dialog_data.get('level_4'))))
            lvl5_name = await session.scalar(select(lvl5_base.level_5).where(lvl5_base.id == int(dialog_manager.current_context().dialog_data.get('level_5'))))
            db_main_items = set(await session.scalars(select(Catalog).where(Catalog.level_5 == lvl5_name, Catalog.level_4 == lvl4_name, Catalog.level_3 == lvl3_name, Catalog.level_2 == lvl2_name)))
            data = {'item': [(f'{item.name.split()[-1]} ({item.price} Руб.)', item.id) for item in db_main_items]}
            return data


#получение карточки товара
async def get_item(dialog_manager: DialogManager, **middleware_data):
     async with async_session() as session:
        db_main = await session.scalar(select(Catalog).where(Catalog.id == int(dialog_manager.current_context().dialog_data.get('item_id'))))
        print(dialog_manager.current_context().dialog_data.get('item_id'))
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
