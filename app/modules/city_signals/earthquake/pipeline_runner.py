from app.core.fetcher import fetch_url, save_raw
from app.core.source_registry import get_source
from app.core.dedup import filter_new_signals
from app.core.pipeline_status import save_pipeline_status

from app.modules.city_signals.earthquake.usgs_parser import parse_usgs_geojson
from app.modules.city_signals.earthquake.filter_region import filter_events
from app.modules.city_signals.earthquake.normalizer import normalize_earthquake_events
from app.modules.city_signals.earthquake.message_render import render_earthquake_signal
from app.core.health_monitor import (
    mark_source_success,
    mark_source_failure,
)

def try_fetch_source(source_id: str, health: dict):
    source = get_source(source_id)

    if not source:
        print("SOURCE NOT FOUND:", source_id)
        health = mark_source_failure(
            health,
            source_id,
            "source not found"
        )
        return None, None, None, health

    print(f"FETCH SOURCE: {source_id}")

    raw_text = fetch_url(source["url"])

    if raw_text is None:
        print(f"SOURCE FAILED: {source_id}")
        health = mark_source_failure(
            health,
            source_id,
            "fetch returned None"
        )
        return source, None, None, health

    saved_path = save_raw(source["id"], raw_text)

    health = mark_source_success(health, source_id)

    print(f"RAW SAVED: {saved_path}")

    return source, raw_text, str(saved_path), health
def fetch_with_fallback(health: dict):
    source, raw_text, saved_path, health = try_fetch_source("koeri", health)

    if raw_text is not None:
        return source, raw_text, saved_path, False, health

    print("KOERI FAILED → TRY USGS")

    source, raw_text, saved_path, health = try_fetch_source("usgs", health)

    return source, raw_text, saved_path, True, health



def run_pipeline(health: dict):
    status = {
        "pipeline": "earthquake",
        "primary_source": "koeri",
        "source_used": None,
        "fallback_used": False,
        "raw_saved": None,
        "events_count": 0,
        "filtered_count": 0,
        "normalized_count": 0,
        "new_signals_count": 0,
        "result": "started",
    }

    source, raw_text, saved_path, fallback_used, health = fetch_with_fallback(health)

    status["fallback_used"] = fallback_used
    status["raw_saved"] = saved_path

    if source:
        status["source_used"] = source.get("id")

    if raw_text is None:
        status["result"] = "all_sources_failed"
        save_pipeline_status(status)
        print("ALL SOURCES FAILED")
        return health

    parser = source.get("parser")

    if parser == "usgs_geojson":
        events = parse_usgs_geojson(raw_text)
    else:
        status["result"] = f"parser_not_implemented:{parser}"
        save_pipeline_status(status)
        print("PARSER NOT IMPLEMENTED:", parser)
        return health

    status["events_count"] = len(events)
    print("RAW EVENTS:", len(events))

    filtered = filter_events(events)
    status["filtered_count"] = len(filtered)
    print("FILTERED EVENTS:", len(filtered))

    signals = normalize_earthquake_events(filtered)
    status["normalized_count"] = len(signals)
    print("NORMALIZED SIGNALS:", len(signals))

    new_signals = filter_new_signals(signals)
    status["new_signals_count"] = len(new_signals)
    print("NEW SIGNALS:", len(new_signals))

    if not new_signals:
        status["result"] = "ok_no_new_signals"
        save_pipeline_status(status)
        print("NO NEW SIGNALS")
        return health

    for signal in new_signals:
        message = render_earthquake_signal(signal)

        print("\nREADY_TO_PUBLISH:\n")
        print(message)
        print()

    status["result"] = "ok_ready_to_publish"
    save_pipeline_status(status)

    return health
if __name__ == "__main__":
    run_pipeline({})