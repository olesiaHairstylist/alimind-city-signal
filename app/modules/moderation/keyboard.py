def build_moderation_keyboard(signal_id: str) -> dict:
    return {
        "inline_keyboard": [
            [
                {
                    "text": "✅ Approve",
                    "callback_data": f"mod:approve:{signal_id}",
                },
                {
                    "text": "❌ Reject",
                    "callback_data": f"mod:reject:{signal_id}",
                },
            ],
            [
                {
                    "text": "⏳ Later",
                    "callback_data": f"mod:later:{signal_id}",
                }
            ],
        ]
    }