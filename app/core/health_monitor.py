from datetime import datetime, timezone


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def mark_source_success(health: dict, source: str) -> dict:
    sources = health.setdefault("sources", {})

    item = sources.setdefault(source, {
        "alive": True,
        "last_success_at": None,
        "last_error_at": None,
        "consecutive_failures": 0,
        "last_error": None,
    })

    item["alive"] = True
    item["last_success_at"] = now_iso()
    item["consecutive_failures"] = 0
    item["last_error"] = None

    return health


def mark_source_failure(health: dict, source: str, error: str) -> dict:
    sources = health.setdefault("sources", {})

    item = sources.setdefault(source, {
        "alive": False,
        "last_success_at": None,
        "last_error_at": None,
        "consecutive_failures": 0,
        "last_error": None,
    })

    item["alive"] = False
    item["last_error_at"] = now_iso()
    item["consecutive_failures"] = item.get("consecutive_failures", 0) + 1
    item["last_error"] = str(error)

    return health