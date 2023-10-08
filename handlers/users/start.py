import asyncpg
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart

from data.config import ADMINS, DRIVER
from keyboards.default.keyboards import *
from loader import dp, db
from states.main_states import Image


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message, state: FSMContext):
    # Retrieve the user
    # global main_menu
    try:
        user = await db.add_user(
            full_name=message.from_user.full_name,
            telegram_id=message.from_user.id,
            # username=message.from_user.username,
        )
    except asyncpg.exceptions.UniqueViolationError:
        user = await db.select_user(telegram_id=message.from_user.id)
    if message.from_user.id == int(ADMINS[0]):
        await message.answer(f"<b>👋 Assalomu alaykum {message.from_user.full_name}!</b>\n\nAdmin sahifaga xush kelibsiz!", reply_markup=admin_main_menu)
    elif message.from_user.id == int(DRIVER):
        await message.answer(f"<b>👋 Assalomu alaykum {message.from_user.full_name}!</b>\n\nYetkazib beruvchi sahifasiga xush kelibsiz!",
                             reply_markup=driver_main_menu)
    else:
        await message.answer(
            f"<b>👋 Assalomu alaykum {message.from_user.full_name}!</b>\n\nBotimizga xush kelibsiz!",
            reply_markup=main_menu)

