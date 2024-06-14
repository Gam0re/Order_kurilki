from aiogram import types, Router, F

from aiogram.filters import Command

from aiogram_dialog import DialogManager, StartMode

catalog_router = Router()

from src.dialogs.Catalog.states import Catalog_levels


@catalog_router.message(Command(commands='catalog'))
@catalog_router.message(F.text == 'Каталог')
async def catalog_lvl1(message: types.Message, dialog_manager: DialogManager):
    await dialog_manager.start(Catalog_levels.level_3, mode=StartMode.RESET_STACK)

@catalog_router.callback_query(F.data == 'to_catalog')
async def catalog_lvl1_answ(callback: types.CallbackQuery, dialog_manager: DialogManager):
    await callback.message.delete()
    await dialog_manager.start(Catalog_levels.level_3, mode=StartMode.RESET_STACK)
