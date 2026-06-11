from app.core.post_cleaner import extract_public_post

from app.core.publish_decisions import (
    set_preview_decision,
    load_pending_previews,
)

from app.core.channel_publisher import (
    publish_to_channel,
    publish_photo_to_channel,
)
def handle_moderation_callback(callback_data: str) -> str:
    parts = callback_data.split(":", 2)

    if len(parts) != 3:
        return "Invalid moderation callback"

    _, action, signal_id = parts

    if action == "approve":
        ok = set_preview_decision(signal_id, "approved")

        if not ok:
            return "Signal not found"

        data = load_pending_previews()

        preview = data.get(signal_id)

        if not preview:
            return "Preview missing"

        public_post = extract_public_post(
            preview["text"]
        )

        signal = preview.get("signal", {})
        image_url = signal.get("image_url", "")

        if image_url:
            result = publish_photo_to_channel(
                image_url,
                public_post,
            )
        else:
            result = publish_to_channel(public_post)

        print("PUBLISH RESULT:", result)

        return "✅ Approved + Published"



