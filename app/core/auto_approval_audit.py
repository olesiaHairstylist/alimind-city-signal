import json
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
AUDIT_PATH = BASE_DIR / "data" / "system" / "auto_approval_audit.jsonl"


def save_auto_approval_audit(signal_id: str, decision: dict, signal: dict) -> None:
    AUDIT_PATH.parent.mkdir(parents=True, exist_ok=True)

    record = {
        "ts": datetime.utcnow().isoformat(),
        "signal_id": signal_id,
        "approved": decision.get("approved"),
        "reason": decision.get("reason"),
        "signal": signal,
    }

    with AUDIT_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")