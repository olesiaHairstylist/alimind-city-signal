from datetime import datetime


def format_time(iso_time: str | None) -> str:
    if not iso_time:
        return "🕒 Time unavailable"

    try:
        dt = datetime.fromisoformat(
            iso_time.replace("Z", "+00:00")
        )
        return f"🕒 {dt.strftime('%H:%M UTC')}"
    except ValueError:
        return "🕒 Time unavailable"


def get_severity_emoji(magnitude: float | None) -> str:
    if magnitude is None:
        return "⚪"

    if magnitude < 3:
        return "🟢"

    if magnitude < 5:
        return "🟡"

    if magnitude < 6:
        return "🟠"

    return "🔴"


def render_earthquake_signal(signal: dict) -> str:
    magnitude = signal.get("magnitude")

    severity = get_severity_emoji(magnitude)

    place = signal.get("place")

    if not place:
        place = "📍 Location unavailable"
    else:
        place = f"📍 {place}"

    event_time = format_time(
        signal.get("event_time_utc")
    )

    source = (
        signal.get("source") or "unknown"
    ).upper()

    return (
        "🌍 Earthquake\n\n"
        f"{severity} M {magnitude}\n"
        f"{place}\n"
        f"{event_time}\n"
        f"📡 Source: {source}"
    )