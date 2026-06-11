import json
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parents[1]

AUTO_PUBLISHED_PATH = (
    BASE_DIR / "data" / "system" / "auto_published.json"
)


def load_auto_published() -> list:
    if not AUTO_PUBLISHED_PATH.exists():
        return []

    try:
        return json.loads(
            AUTO_PUBLISHED_PATH.read_text(
                encoding="utf-8"
            )
        )

    except Exception:
        return []


def save_auto_published(
    signal_id: str,
    reason: str,
) -> None:
    existing = load_auto_published()

    existing.append({
        "signal_id": signal_id,
        "published_at": datetime.utcnow().isoformat(),
        "mode": "auto",
        "reason": reason,
    })

    AUTO_PUBLISHED_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    AUTO_PUBLISHED_PATH.write_text(
        json.dumps(
            existing,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )


def was_auto_published(signal_id: str) -> bool:
    existing = load_auto_published()

    for item in existing:
        if item.get("signal_id") == signal_id:
            return True

    return False