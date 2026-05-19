import json


def parse_usgs_geojson(raw_text: str):
    data = json.loads(raw_text)

    events = []

    for feature in data.get("features", []):
        props = feature.get("properties", {})
        geometry = feature.get("geometry", {})
        coordinates = geometry.get("coordinates", [])

        if len(coordinates) < 2:
            continue

        lon = coordinates[0]
        lat = coordinates[1]

        event = {
            "source": "usgs",
            "external_id": feature.get("id"),
            "place": props.get("place"),
            "magnitude": props.get("mag"),
            "time_ms": props.get("time"),
            "lat": lat,
            "lon": lon,
            "depth_km": coordinates[2] if len(coordinates) > 2 else None,
            "url": props.get("url"),
        }

        events.append(event)

    return events