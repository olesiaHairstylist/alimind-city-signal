from datetime import datetime, timezone


def parse_iso(value: str):
    if not value:
        return None

    try:
        return datetime.fromisoformat(value)
    except Exception:
        return None


def is_stale_iso(value: str, max_age_seconds: int) -> bool:
    dt = parse_iso(value)

    if dt is None:
        return True

    now = datetime.now(timezone.utc)

    age = now - dt

    return age.total_seconds() > max_age_seconds