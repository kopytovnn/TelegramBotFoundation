import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from database.models.user import *
from Conditions import *

TOKEN = "5884056129:AAGA_c-KAS4-BIsNKkmjRffFp2_TAGfP04A"

dp = Dispatcher()

engine = create_engine("sqlite:///database/Data.db")
Base.metadata.create_all(engine)


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    telegram_id = message.from_user.id
    if UserIsRegistered(telegram_id).check():
        await message.answer(f"И снова здравствуй, {hbold(message.from_user.full_name)}!")
    else:
        user = User(telegram_id=telegram_id,
                    status="user")
        with Session(engine) as session:
            session.add_all([user])
            session.commit()
        await message.answer(f"Здравствуй, {hbold(message.from_user.full_name)}!")



@dp.message()
async def echo_handler(message: types.Message) -> None:
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        # But not all the types is supported to be copied so need to handle it
        await message.answer("Nice try!")


async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())