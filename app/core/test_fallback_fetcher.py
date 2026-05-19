from app.core.fetcher import fetch_url, save_raw
from app.core.source_registry import get_source


def try_fetch_source(source_id: str):
    source = get_source(source_id)

    if not source:
        print("SOURCE NOT FOUND:", source_id)
        return None

    print("TRY SOURCE:", source_id)

    raw_text = fetch_url(source["url"])

    if raw_text is None:
        print("SOURCE FAILED:", source_id)
        return None

    saved_path = save_raw(source["id"], raw_text)

    print("SOURCE OK:", source_id)
    print("RAW LENGTH:", len(raw_text))
    print("RAW SAVED:", saved_path)

    return raw_text


def main():
    raw_text = try_fetch_source("koeri")

    if raw_text is None:
        print("KOERI FAILED → TRY FALLBACK USGS")
        raw_text = try_fetch_source("usgs")

    if raw_text is None:
        print("ALL SOURCES FAILED")
        return

    print("FALLBACK_USGS_V1 OK")


if __name__ == "__main__":
    main()