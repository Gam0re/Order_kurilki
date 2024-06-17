from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import (
    Back,
    Button,
    Row,
    ScrollingGroup,
    Select
)
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.media import DynamicMedia, StaticMedia
from aiogram.types import ContentType
import operator

from src.handlers.order_registration import sending_order

from .states import Catalog_levels
from .getters import get_level_4, get_level_5, get_level_3, get_item, get_selected_items
from .callbacks import selected_level3, selected_level4, selected_level5, \
    selected_item3, to_item, back, selected_item4,selected_item5, to_cart, to_main, go_to_cart, increment, decrement, quant



Catalog_lvl1 = Dialog(
    Window(
        Const("Пожалуйста, выберите бренд"),
        ScrollingGroup(
            Select(
                id="Level_3",
                items="lvl3",
                item_id_getter=operator.itemgetter(1),
                text=Format("{item[0]}"),
                on_click=selected_level3,
            ),
            id="lvl3_group",
            height=10,
            width=1,
            hide_on_single_page=True
        ),
        Button(Const("На главную"), id="to_main", on_click=to_main),
        state=Catalog_levels.level_3,
        getter=get_level_3,
    ),
    Window(
        Const("Пожалуйста, выберите количество затяжек"),
        ScrollingGroup(
            Select(
                id="Level_4",
                items="lvl4",
                item_id_getter=operator.itemgetter(1),
                text=Format("{item[0]}"),
                on_click=selected_level4,
            ),
            id="lvl4_group",
            height=10,
            width=1,
            hide_on_single_page=True
        ),
        Button(Const("На главную"), id="to_main", on_click=to_main),
        Back(Const("⬅ Назад")),
        state=Catalog_levels.level_4,
        getter=get_level_4,
    ),
    Window(
        Const("Пожалуйста, выберите вкус"),
        ScrollingGroup(
            Select(
                id="Level_5",
                items="lvl5",
                item_id_getter=operator.itemgetter(1),
                text=Format("{item[0]}"),
                on_click=to_item,
            ),
            id="lvl5_group",
            height=10,
            width=1,
            hide_on_single_page=True
        ),
        Button(Const("На главную"), id="to_main", on_click=to_main),
        Back(Const("⬅ Назад")),
        state=Catalog_levels.level_5,
        getter=get_level_5,
    ),
    Window(
        StaticMedia(
        path=Format('{image}'),
        type=ContentType.PHOTO,
    ),
        Format("Вы выбрали: {brand}\n"
               "Кол-во затяжек: до {puffs}\n"
               "Вкус: {flavor}\n"
               "Объем жидкости: {volume} мл\n"
               "Содержание никотина: {nicotine}\n"
               "Нагревательных элеметов: {heat_element}\n"
               "Батарея: {battery} мАч\n"
               "Разъём для зарядки: {connector}\n"
               "Состав: {compound}\n"
               "\nКоличество выбранного товара уточняйте у менеджера!"
               ),
        Row(Button(Const("На главную"), id="to_main", on_click=to_main), Button(Const("В корзину"), id='to_cart', on_click=to_cart),
            Back(Const("⬅ Назад"))),
        state=Catalog_levels.item,
        getter=get_item,
    ),
)


