from app.modules.city_signals.earthquake.message_render import (
    render_earthquake_signal,
)


def main():
    signal = {
        "signal_id": "usgs:test001",
        "category": "earthquake",
        "source": "usgs",
        "external_id": "test001",
        "title": "M3.1 earthquake",
        "place": "Gazipasa / Antalya",
        "magnitude": 3.1,
        "lat": 36.72,
        "lon": 32.18,
        "depth_km": 8.4,
        "event_time_utc": "2026-05-19T08:34:00+00:00",
        "confidence": "verified",
        "status": "new",
        "source_url": "https://example.com",
    }

    message = render_earthquake_signal(signal)

    print(message)

    print("SIGNAL_MESSAGE_RENDER_V1 OK")


if __name__ == "__main__":
    main()