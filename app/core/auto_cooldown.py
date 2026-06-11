import json
from pathlib import Path
from datetime import datetime


BASE_DIR = Path(__file__).resolve().parents[1]

AUTO_COOLDOWN_PATH = (
    BASE_DIR / "data" / "system" / "auto_cooldown.json"
)


def load_recent_auto_posts() -> list:
    if not AUTO_COOLDOWN_PATH.exists():
        return []

    try:
        return json.loads(
            AUTO_COOLDOWN_PATH.read_text(
                encoding="utf-8"
            )
        )

    except Exception:
        return []


def save_auto_publish_timestamp() -> None:
    data = load_recent_auto_posts()

    data.append(
        datetime.utcnow().isoformat()
    )

    AUTO_COOLDOWN_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    AUTO_COOLDOWN_PATH.write_text(
        json.dumps(
            data,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )


def is_cooldown_triggered(
    max_posts: int = 2,
) -> bool:
    data = load_recent_auto_posts()

    return len(data) >= max_posts