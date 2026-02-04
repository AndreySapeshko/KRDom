from aiogram import Router
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, WebAppInfo

router = Router()


@router.message(Command("start"))
async def start_cmd(message: Message):
    print(f"ENTER start_cmd telegram_id: {message.from_user.id}")

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🧮 Калькулятор KR.Dom",
                    web_app=WebAppInfo(url="https://frame-dom.ru"),
                )
            ]
        ]
    )

    await message.answer("👋 Привет!\n\nОткрой калькулятор:", reply_markup=kb)
