import hmac
import time
import json
import urllib.parse
from hashlib import sha256

from fastapi import Depends, Header, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.config import TELEGRAM_BOT_TOKEN
from backend.db.models.user import User
from backend.db.session import get_session


def verify_telegram_init_data(init_data: str) -> dict:
    print("ENTER verify_telegram_init_data")
    parsed = dict(urllib.parse.parse_qsl(init_data, keep_blank_values=True))
    if "hash" not in parsed:
        print("Invalid Telegram initData")
        raise HTTPException(status_code=401, detail="Invalid Telegram initData")

    received_hash = parsed.pop("hash")

    data_check_string = "\n".join(f"{k}={v}" for k, v in sorted(parsed.items()))
    secret_key = hmac.new(b"WebAppData", TELEGRAM_BOT_TOKEN.encode(), sha256).digest()

    calculated_hash = hmac.new(secret_key, data_check_string.encode(), sha256).hexdigest()

    if calculated_hash != received_hash:
        print("Invalid Telegram signature")
        raise HTTPException(status_code=401, detail="Invalid Telegram signature")

    auth_date = int(parsed.get("auth_date", 0))
    now = int(time.time())

    if abs(now - auth_date) > 86400:
        print("Telegram auth expired")
        raise HTTPException(status_code=401, detail="Telegram auth expired")

    user = parsed.get("user")
    if not user:
        print("No Telegram user")
        raise HTTPException(status_code=401, detail="No Telegram user")

    return json.loads(user)  # user = JSON string


async def get_current_user(
    x_telegram_initdata: str = Header(None, alias="X-Telegram-InitData"),
    session: AsyncSession = Depends(get_session),
) -> User:
    print("ENTER get_current_telegram_user")
    tg_user = verify_telegram_init_data(x_telegram_initdata)

    stmt = select(User).where(User.telegram_id == tg_user["id"])
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        user = User(
            telegram_id=tg_user["id"],
            username=tg_user.get("username"),
            is_active=True,
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)

    return user
