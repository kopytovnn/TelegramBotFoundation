import asyncio
import logging
import sys
from os import getenv
from jinja2 import Environment, FileSystemLoader

from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup
from aiogram.utils.markdown import hbold
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import F

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from database.models.user import *
from Conditions import *
from messages import buttons

TOKEN = ""

dp = Dispatcher()

engine = create_engine("sqlite:///database/Data.db")
Base.metadata.create_all(engine)


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """

    telegram_id = message.from_user.id
    environment = Environment(loader=FileSystemLoader("messages/"))
    template = environment.get_template("Greeting.html")

    if not UserIsRegistered(telegram_id).check():
        user = User(telegram_id=telegram_id,
                    status="user")
        with Session(engine) as session:
            session.add_all([user])
            session.commit()

    builder = InlineKeyboardBuilder()
    builder.add(buttons.CHECK_BY_PHOTO,
                buttons.TARIFES,
                buttons.EXAMPLES,
                buttons.LK,
                buttons.SUPPORT
    )

    await message.answer(template.render(), reply_markup=builder.as_markup())


@dp.callback_query(F.data == 'support')
async def suppot(callback: types.CallbackQuery):
    await callback.message.answer(str((1, 10)))


@dp.callback_query(F.data == 'personal_account')
async def personal_account(callback: types.CallbackQuery):
    telegram_id = callback.message.from_user.id
    environment = Environment(loader=FileSystemLoader("messages/"))
    template = environment.get_template("PersonalAccount.html", {"telegram_id": telegram_id})
    template.render()
    await callback.message.answer(template.render())


async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
