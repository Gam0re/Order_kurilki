from aiogram import types, Router, F

from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

from aiogram_dialog import DialogManager

import src.database.requests as rq
import src.keyboards.default.reply as kb

faq_router = Router()


@faq_router.message(F.text == 'Вопросы и ответы')
async def to_faq(message: types.Message, state: FSMContext, dialog_manager: DialogManager):
    try:
        await dialog_manager.done()
    except:
        pass
    await message.answer("Вы перешли в раздел с вопросами и ответами.\nВыберите необходимую опцию", reply_markup=kb.faq_kb)


@faq_router.message(F.text == 'Общие вопросы')
async def to_general_questions(message: types.Message):
    await message.answer("Выберете интересующий вас вопрос", reply_markup=kb.questions_kb)


@faq_router.message(F.text == 'Наши контакты')
async def to_general_questions(message: types.Message):
    await message.answer("Менеджер: @hotsmok_cn_7; +7 981 045 55 10"
                         "\nОфис: г. Санкт-Петербург, 18 линия В. О., д. 29, лит. И, офис 513"
                         "\nСоц. сети:"
                         "\n- Telegram: https://t.me/hotsmok_cn"
                         "\n- VK: https://vk.com/hotsmok_cn", reply_markup=kb.faq_kb)

@faq_router.message(F.text == 'Как сделать заказ?')
async def how_to_order(message: types.Message):
    await message.answer('Телеграмм: @hotsmok_cn_7\nПожалуйста, направьте Ваш вопрос нашему менеджеру. Мы ответим Вам в течение 24 часов.', reply_markup=kb.questions_kb)

@faq_router.message(F.text == 'Какие бренды поставляет наша компания?')
async def brands(message: types.Message):
    await message.answer('SEABEAR:\nДанный бренд высококачественных электронных сигарет сочетает в себе минималистичный дизайн и концепцию защиты окружающей среды.'
                         '\nPUFF:\nПроводит постоянные исследования различных форм парения, стремится добиться идеального баланса между пользой для здоровья и ярким вкусом.'
                         '\nEPE:\nЯвляется одним из лидеров в отрасли, который проводит исследования технологий производства электронных сигарет, предоставляя потребителю широкий выбор устройств для парения.'
                         '\nAIRSTICK:\nКлиент - главный приоритет, поэтому бренд старается произвести товар, превосходящий самые смелые ожидания потребителя.'
                         '\nCAMOBAR:\nПродукция данного бренда является воплощением технологий и искусства, удовлетворяя стремления потребителя к лучшему качеству жизни.'
                         '\nVAPGO BAR:\nУделяет особое внимание контролю над производственным процессом для обеспечения безопасности и эффективности каждого устройства.', reply_markup=kb.questions_kb)