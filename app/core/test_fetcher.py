from app.core.fetcher import (
    fetch_url,
    save_raw,
)

from app.core.source_registry import (
    get_source,
)


def main():
    source = get_source("koeri")

    if not source:
        raise RuntimeError(
            "KOERI source not found"
        )

    print("FETCHING...")

    raw_text = fetch_url(
        source["url"]
    )

    if raw_text is None:
        print("FETCH_CORE_V1 FAILED: source unavailable")
        return

    print(
        "RAW LENGTH:",
        len(raw_text)
    )

    saved_path = save_raw(
        source["id"],
        raw_text,
    )

    print(
        "RAW SAVED:",
        saved_path
    )

    print("FETCH_CORE_V1 OK")


if __name__ == "__main__":
    main()