import json
from datetime import datetime
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]

AUTO_REVIEW_PANEL_PATH = (
    BASE_DIR / "data" / "system" / "auto_review_panel.json"
)


def load_auto_review_panel() -> list:
    if not AUTO_REVIEW_PANEL_PATH.exists():
        return []

    try:
        return json.loads(
            AUTO_REVIEW_PANEL_PATH.read_text(encoding="utf-8")
        )
    except Exception:
        return []


def save_auto_review_item(
    signal_id: str,
    reason: str,
    source: str = "unknown",
) -> None:
    panel = load_auto_review_panel()

    panel.append(
        {
            "timestamp": datetime.utcnow().isoformat(),
            "signal_id": signal_id,
            "reason": reason,
            "source": source,
            "action": "manual_review",
        }
    )

    AUTO_REVIEW_PANEL_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    AUTO_REVIEW_PANEL_PATH.write_text(
        json.dumps(
            panel,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )