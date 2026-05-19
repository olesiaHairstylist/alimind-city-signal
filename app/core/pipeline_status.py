import json
from pathlib import Path
from datetime import datetime


BASE_DIR = Path(__file__).resolve().parents[1]

STATUS_PATH = (
    BASE_DIR
    / "data"
    / "system"
    / "pipeline_status.json"
)


def ensure_status_file():
    STATUS_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    if not STATUS_PATH.exists():
        STATUS_PATH.write_text(
            "{}",
            encoding="utf-8",
        )


def save_pipeline_status(status: dict):
    ensure_status_file()

    status["updated_at"] = (
        datetime.utcnow().isoformat()
    )

    STATUS_PATH.write_text(
        json.dumps(
            status,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )


def load_pipeline_status():
    ensure_status_file()

    raw = STATUS_PATH.read_text(
        encoding="utf-8",
    )

    return json.loads(raw)