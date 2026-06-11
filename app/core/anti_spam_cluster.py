import json
from datetime import datetime, timedelta
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]

CLUSTER_HISTORY_PATH = (
    BASE_DIR / "data" / "system" / "cluster_history.json"
)

CLUSTER_WINDOW_MINUTES = 60


def load_cluster_history() -> list:
    if not CLUSTER_HISTORY_PATH.exists():
        return []

    try:
        return json.loads(
            CLUSTER_HISTORY_PATH.read_text(encoding="utf-8")
        )
    except Exception:
        return []


def save_cluster_history_item(signal: dict) -> None:
    history = load_cluster_history()

    history.append(
        {
            "timestamp": datetime.utcnow().isoformat(),
            "category": signal.get("category", "unknown"),
            "location": signal.get("location", "unknown"),
        }
    )

    CLUSTER_HISTORY_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    CLUSTER_HISTORY_PATH.write_text(
        json.dumps(
            history,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )


def normalize_cluster_key(signal: dict) -> str:
    category = signal.get("category", "unknown")
    location = signal.get("location", "unknown")

    return f"{category}:{location}".lower().strip()


def is_cluster_blocked(signal: dict) -> bool:
    history = load_cluster_history()

    if not history:
        return False

    current_key = normalize_cluster_key(signal)

    limit_time = (
        datetime.utcnow()
        - timedelta(minutes=CLUSTER_WINDOW_MINUTES)
    )

    for item in history:
        try:
            item_time = datetime.fromisoformat(item["timestamp"])
        except Exception:
            continue

        item_key = normalize_cluster_key(item)

        if item_time > limit_time and item_key == current_key:
            return True

    return False