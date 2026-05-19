import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]

PUBLISHED_SIGNALS_PATH = (
    BASE_DIR
    / "data"
    / "system"
    / "published_signals.json"
)


def ensure_storage():
    PUBLISHED_SIGNALS_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    if not PUBLISHED_SIGNALS_PATH.exists():
        PUBLISHED_SIGNALS_PATH.write_text(
            "[]",
            encoding="utf-8",
        )


def load_published_ids() -> set[str]:
    ensure_storage()

    raw = PUBLISHED_SIGNALS_PATH.read_text(
        encoding="utf-8",
    )

    data = json.loads(raw)

    return set(data)


def save_published_ids(ids: set[str]):
    ensure_storage()

    PUBLISHED_SIGNALS_PATH.write_text(
        json.dumps(
            sorted(ids),
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )


def is_new_signal(signal: dict) -> bool:
    signal_id = signal.get("signal_id")

    if not signal_id:
        return False

    published_ids = load_published_ids()

    return signal_id not in published_ids


def mark_signal_published(signal: dict):
    signal_id = signal.get("signal_id")

    if not signal_id:
        return

    published_ids = load_published_ids()
    published_ids.add(signal_id)
    save_published_ids(published_ids)


def filter_new_signals(signals: list[dict]) -> list[dict]:
    return [
        signal
        for signal in signals
        if is_new_signal(signal)
    ]