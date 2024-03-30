from aiogram import Bot, Dispatcher, Router, types


CHECK_BY_PHOTO = types.InlineKeyboardButton(
        text="Проверить по фото",
        callback_data="check_by_photo")
TARIFES = types.InlineKeyboardButton(
        text="Тарифы",
        callback_data="tarifes")
LK = types.InlineKeyboardButton(
        text="Личный кабинет",
        callback_data="personal_account")
EXAMPLES = types.InlineKeyboardButton(
        text="Примеры",
        callback_data="examples")
SUPPORT = types.InlineKeyboardButton(
        text="Поддержка",
        callback_data="support")
