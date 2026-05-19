from datetime import datetime, timezone


def ms_to_iso(time_ms: int | None) -> str | None:
    if time_ms is None:
        return None

    dt = datetime.fromtimestamp(
        time_ms / 1000,
        tz=timezone.utc,
    )

    return dt.isoformat()


def normalize_earthquake_event(event: dict) -> dict:
    source = event.get("source")
    external_id = event.get("external_id")

    return {
        "signal_id": f"{source}:{external_id}",
        "category": "earthquake",
        "source": source,
        "external_id": external_id,
        "title": f"M{event.get('magnitude')} earthquake",
        "place": event.get("place"),
        "magnitude": event.get("magnitude"),
        "lat": event.get("lat"),
        "lon": event.get("lon"),
        "depth_km": event.get("depth_km"),
        "event_time_utc": ms_to_iso(
            event.get("time_ms")
        ),
        "confidence": "verified",
        "status": "new",
        "source_url": event.get("url"),
    }


def normalize_earthquake_events(events: list[dict]) -> list[dict]:
    return [
        normalize_earthquake_event(event)
        for event in events
    ]