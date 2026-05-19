from datetime import datetime


def format_time(iso_time: str | None) -> str:
    if not iso_time:
        return "время не указано"

    try:
        dt = datetime.fromisoformat(
            iso_time.replace("Z", "+00:00")
        )
        return dt.strftime("%H:%M UTC")
    except ValueError:
        return iso_time


def render_earthquake_signal(signal: dict) -> str:
    magnitude = signal.get("magnitude")
    place = signal.get("place") or "место не указано"
    event_time = format_time(signal.get("event_time_utc"))
    source = (signal.get("source") or "unknown").upper()

    return (
        "🌍 Землетрясение\n\n"
        f"M{magnitude}\n"
        f"{place}\n"
        f"{event_time}\n\n"
        f"Источник: {source}"
    )