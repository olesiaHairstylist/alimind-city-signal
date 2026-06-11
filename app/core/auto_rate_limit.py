from datetime import datetime, timedelta

from app.core.auto_cooldown import (
    load_recent_auto_posts,
)

RATE_LIMIT_MINUTES = 30


def get_last_auto_publish_time():
    posts = load_recent_auto_posts()

    if not posts:
        return None

    latest = max(posts)

    try:
        return datetime.fromisoformat(latest)
    except Exception:
        return None


def is_rate_limit_triggered() -> bool:
    last_time = get_last_auto_publish_time()

    if last_time is None:
        return False

    limit_time = (
            datetime.utcnow()
        - timedelta(minutes=RATE_LIMIT_MINUTES)
    )

    return last_time > limit_time