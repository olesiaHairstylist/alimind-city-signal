import json
from pathlib import Path


STATE_PATH = Path(
    "app/data/system/control_state.json"
)


def load_control_state() -> dict:
    if not STATE_PATH.exists():
        return {}

    try:
        with open(STATE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)

    except Exception:
        print("CONTROL STATE CORRUPTED")
        return {}


def save_control_state(state: dict) -> None:
    STATE_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(
            state,
            f,
            ensure_ascii=False,
            indent=2,
        )
