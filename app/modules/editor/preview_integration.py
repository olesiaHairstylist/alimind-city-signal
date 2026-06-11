from app.modules.editor.ai_editor import (
    generate_editor_draft,
)

from app.modules.editor.validator import (
    validate_editor_draft,
)

from app.core.preview_sender import (
    send_preview_message,
)
from app.modules.editor.signal_quality import (
    validate_signal_quality,
)

def process_editor_preview(raw_message: str) -> dict:
    signal_validation = validate_signal_quality(raw_message)

    if not signal_validation["ok"]:
        return {
            "ok": False,
            "stage": "signal_quality",
            "errors": signal_validation["errors"],
        }

    draft = generate_editor_draft(raw_message)

    validation = validate_editor_draft(draft)

    if not validation["ok"]:
        return {
            "ok": False,
            "stage": "draft_validation",
            "errors": validation["errors"],
            "warnings": validation["warnings"],
        }

    preview_text = draft

    if validation["warnings"]:
        preview_text += "\n\n🟡 Editorial warnings:\n"

        for warning in validation["warnings"]:
            preview_text += (
                f"- {warning['type']} "
                f"({warning['severity']}): "
                f"{warning['message']}\n"
            )

    send_preview_message(preview_text)

    return {
        "ok": True,
        "draft": draft,
        "warnings": validation["warnings"],
    }