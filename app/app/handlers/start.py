from aiogram import Router
from aiogram import F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from dependency_injector.wiring import inject, Provide

from app.core.container import Container
from app.services.telegram_user_service import TelegramUserService

from app.schemas.telegram_user import TelegramUserEntity
from app.keyboards.keyboards import send_word_keyboard
from app.states.state import Form
from app.utils import const

from loguru import logger

start_router = Router()


@start_router.message(CommandStart())
@inject
async def command_start(
    message: Message,
    telegram_user_service: TelegramUserService = Provide[
        Container.telegram_user_service
    ],
) -> None:
    user_dict = message.from_user.model_dump()
    user_id = user_dict.pop("id")

    user_dict["user_id"] = user_id

    user = TelegramUserEntity(**user_dict)

    # await telegram_user_service.create_telegram_user(user=user)
    await message.answer(const.START_MESSAGE.format(first_name=user.first_name), reply_markup=send_word_keyboard)


@start_router.callback_query(F.data == "send_word")
async def send_word_handler(callback_query: CallbackQuery, state: FSMContext) -> None:
    await callback_query.message.delete_reply_markup()

    await callback_query.message.answer(const.SEND_WORD)

    await state.set_state(Form.word)


@start_router.message(Form.word)
async def process_word(message: Message, state: FSMContext) -> None:
    msg = message.text.lower()

    verb = const.irregular_verbs.get(msg)
    if verb:
        await message.answer("Ваши глаголы: " + ", ".join(verb))
        await state.clear()
    else:
        await message.answer("Не смогли найти такой глагол, проверьте корректность его написания и отправьте снова)")
