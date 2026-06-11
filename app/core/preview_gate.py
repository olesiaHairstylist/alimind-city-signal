
from app.core.preview_sender import send_preview_message

def build_preview_item(signal: dict, message: str) -> dict:
    return {
        "status": "waiting_review",
        "channel": "telegram",
        "signal_id": signal.get("id"),
        "message": message,
        "approved": False,
        "published": False,
    }


def print_preview_item(item: dict) -> None:
    print("\n=== TELEGRAM PREVIEW GATE ===")
    print("STATUS:", item.get("status"))
    print("CHANNEL:", item.get("channel"))
    print("SIGNAL ID:", item.get("signal_id"))
    print("\nMESSAGE:\n")
    print(item.get("message"))
    send_preview_message(item.get("message", ""))
    print("\nAPPROVED:", item.get("approved"))
    print("PUBLISHED:", item.get("published"))