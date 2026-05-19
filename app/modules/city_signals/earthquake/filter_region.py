ALANYA_REGION = {
    "min_lat": 36.0,
    "max_lat": 37.5,
    "min_lon": 31.5,
    "max_lon": 33.5,
}


MIN_MAGNITUDE = 2.5


def is_in_region(event: dict) -> bool:
    lat = event.get("lat")
    lon = event.get("lon")

    if lat is None or lon is None:
        return False

    return (
        ALANYA_REGION["min_lat"]
        <= lat
        <= ALANYA_REGION["max_lat"]
        and
        ALANYA_REGION["min_lon"]
        <= lon
        <= ALANYA_REGION["max_lon"]
    )


def is_valid_magnitude(event: dict) -> bool:
    magnitude = event.get("magnitude")

    if magnitude is None:
        return False

    return magnitude >= MIN_MAGNITUDE


def filter_events(events: list[dict]):
    filtered = []

    for event in events:
        if not is_in_region(event):
            continue

        if not is_valid_magnitude(event):
            continue

        filtered.append(event)

    return filtered