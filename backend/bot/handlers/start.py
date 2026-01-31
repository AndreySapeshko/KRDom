from aiogram import Router
from aiogram.filters import Command
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup, WebAppInfo

router = Router()


@router.message(Command("start"))
async def start_cmd(message: Message):
    print(f"ENTER start_cmd telegram_id: {message.from_user.id}")

    kb = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text="🧮 Калькулятор KR.Dom",
                    web_app=WebAppInfo(url="https://ebony-administrative-pit-associated.trycloudflare.com"),
                )
            ]
        ],
        resize_keyboard=True,
    )

    await message.answer("👋 Привет!\n\nОткрой калькулятор:", reply_markup=kb)
