import os
import requests
from app.modules.moderation.keyboard import build_moderation_keyboard
from dotenv import load_dotenv
load_dotenv()

def send_admin_preview(signal_id: str, text: str) -> bool:
    bot_token = os.getenv("BOT_TOKEN")
    admin_chat_id = os.getenv("ADMIN_CHAT_ID")

    if not bot_token:
        print("TELEGRAM PREVIEW ERROR: BOT_TOKEN missing")
        return False

    if not admin_chat_id:
        print("TELEGRAM PREVIEW ERROR: ADMIN_CHAT_ID missing")
        return False

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

    payload = {
        "chat_id": admin_chat_id,
        "text": text,
        "reply_markup": build_moderation_keyboard(signal_id),
        "disable_web_page_preview": True,
    }

    try:
        response = requests.post(
            url,
            json=payload,
            timeout=10,
        )

        if response.status_code != 200:
            print("TELEGRAM PREVIEW ERROR:", response.text)
            return False

        print("TELEGRAM PREVIEW SENT")
        return True

    except Exception as e:
        print("TELEGRAM PREVIEW CRASH:", e)
        return False