TRUSTED_AUTO_SOURCES = {
    "usgs": True,
    "koeri": True,
}


def get_signal_source(signal: dict) -> str:
    return (
        signal.get("source")
        or signal.get("source_name")
        or "unknown"
    ).lower().strip()


def is_source_trusted_for_auto(signal: dict) -> bool:
    source = get_signal_source(signal)

    return TRUSTED_AUTO_SOURCES.get(source, False)