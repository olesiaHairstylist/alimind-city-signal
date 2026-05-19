from app.core.dedup import (
    is_new_signal,
    mark_signal_published,
    filter_new_signals,
)


def main():
    signal = {
        "signal_id": "test:earthquake:001",
        "category": "earthquake",
        "title": "Test earthquake",
    }

    print("FIRST CHECK:", is_new_signal(signal))

    mark_signal_published(signal)

    print("SECOND CHECK:", is_new_signal(signal))

    signals = [
        signal,
        {
            "signal_id": "test:earthquake:002",
            "category": "earthquake",
            "title": "Second test earthquake",
        },
    ]

    new_signals = filter_new_signals(signals)

    print("NEW SIGNALS COUNT:", len(new_signals))

    for item in new_signals:
        print(item)

    print("DEDUP_V1 OK")


if __name__ == "__main__":
    main()