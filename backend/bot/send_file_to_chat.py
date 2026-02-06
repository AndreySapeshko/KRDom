from aiogram.types import BufferedInputFile

from backend.bot.bot import bot


async def send_pdf_report(chat_id: int, pdf_bytes: bytes, filename: str):
    file = BufferedInputFile(pdf_bytes, filename=filename)

    await bot.send_document(chat_id=chat_id, document=file, caption="Ваш отчёт KR.Dom готов 📄")
