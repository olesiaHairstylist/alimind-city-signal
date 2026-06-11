import os
import requests
from dotenv import load_dotenv

load_dotenv()


def publish_to_channel(text: str) -> bool:
    bot_token = os.getenv("BOT_TOKEN")
    channel_id = os.getenv("SIGNAL_CHANNEL_ID")

    if not bot_token:
        print("CHANNEL PUBLISH ERROR: BOT_TOKEN missing")
        return False

    if not channel_id:
        print("CHANNEL PUBLISH ERROR: SIGNAL_CHANNEL_ID missing")
        return False

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

    payload = {
        "chat_id": channel_id,
        "text": text,
        "disable_web_page_preview": True,
    }

    try:
        response = requests.post(
            url,
            json=payload,
            timeout=10,
        )

        if response.status_code != 200:
            print("CHANNEL PUBLISH ERROR:", response.text)
            return False

        print("CHANNEL PUBLISHED")
        return True

    except Exception as e:
        print("CHANNEL PUBLISH CRASH:", e)
        return False

def publish_photo_to_channel(
        photo_url: str,
        caption: str,
) -> bool:

    bot_token = os.getenv("BOT_TOKEN")
    channel_id = os.getenv("SIGNAL_CHANNEL_ID")

    if not bot_token:
        print("CHANNEL PHOTO ERROR: BOT_TOKEN missing")
        return False

    if not channel_id:
        print("CHANNEL PHOTO ERROR: SIGNAL_CHANNEL_ID missing")
        return False

    url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"

    payload = {
        "chat_id": channel_id,
        "photo": photo_url,
        "caption": caption[:1024],
    }

    try:
        response = requests.post(
            url,
            json=payload,
            timeout=20,
        )

        if response.status_code != 200:
            print("CHANNEL PHOTO ERROR:", response.text)
            return False

        print("CHANNEL PHOTO PUBLISHED")
        return True

    except Exception as e:
        print("CHANNEL PHOTO CRASH:", e)
        return False