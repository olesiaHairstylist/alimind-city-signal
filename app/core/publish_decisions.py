import json
from pathlib import Path
from datetime import datetime, UTC


BASE_DIR = Path(__file__).resolve().parents[2]
PENDING_PATH = BASE_DIR / "app" / "data" / "system" / "pending_previews.json"


def load_pending_previews() -> dict:
    if not PENDING_PATH.exists():
        return {}

    try:
        with open(PENDING_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        print("PENDING PREVIEWS CORRUPTED")
        return {}


def save_pending_previews(data: dict) -> None:
    PENDING_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(PENDING_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def add_pending_preview(signal_id: str, text: str, signal: dict) -> None:

    data = load_pending_previews()

    data[signal_id] = {
        "signal_id": signal_id,
        "status": "pending",
        "text": text,
        "signal": signal,
        "created_at": datetime.now(UTC).isoformat(),
        "decided_at": None,
    }

    save_pending_previews(data)


def set_preview_decision(signal_id: str, decision: str) -> bool:
    print("PENDING PATH:", PENDING_PATH)
    print("DECISION SIGNAL:", signal_id)
    data = load_pending_previews()

    if signal_id not in data:
        return False

    data[signal_id]["status"] = decision
    data[signal_id]["decided_at"] = datetime.now(UTC).isoformat()

    save_pending_previews(data)
    return True