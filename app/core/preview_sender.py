import os
import requests
from dotenv import load_dotenv
from app.modules.moderation.keyboard import (
    build_moderation_keyboard,
)
load_dotenv()


def send_preview_message(
    signal_id: str,
    text: str,
    chat_id: int | None = None,
) -> dict:
    bot_token = os.getenv("BOT_TOKEN")
    target_chat_id = chat_id or os.getenv("PREVIEW_CHAT_ID")

    if not bot_token:
        raise RuntimeError("BOT_TOKEN not found")

    if not target_chat_id:
        raise RuntimeError("PREVIEW_CHAT_ID not found")

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

    response = requests.post(
        url,
        json={
            "chat_id": target_chat_id,
            "text": text,
            "reply_markup": build_moderation_keyboard(signal_id),
        },
        timeout=30,
    )

    return response.json()