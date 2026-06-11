from app.core.fetcher import fetch_url, save_raw
from app.core.source_registry import get_source
from app.core.dedup import filter_new_signals
from app.core.pipeline_status import save_pipeline_status
from app.core.preview_gate import (
    build_preview_item,
    print_preview_item,
)
from app.modules.editor.validator import validate_editor_draft
from app.modules.city_signals.earthquake.usgs_parser import parse_usgs_geojson
from app.modules.city_signals.earthquake.filter_region import filter_events
from app.core.telegram_preview_gate import send_admin_preview
from app.core.auto_approval_audit import save_auto_approval_audit
from app.modules.city_signals.earthquake.normalizer import normalize_earthquake_events
from app.core.publish_decisions import add_pending_preview
from app.core.auto_approval import should_auto_approve
from app.modules.city_signals.earthquake.message_render import render_earthquake_signal
from app.core.auto_published_store import (
    was_auto_published,
    save_auto_published,
)
from app.core.health_monitor import (
    mark_source_success,
    mark_source_failure,
)
from app.core.auto_cooldown import (
    is_cooldown_triggered,
    save_auto_publish_timestamp,
)
from app.core.auto_cooldown import (
    is_cooldown_triggered,
    save_auto_publish_timestamp,
)
from app.core.auto_rate_limit import (
    is_rate_limit_triggered,
)
from app.core.anti_spam_cluster import (
    is_cluster_blocked,
    save_cluster_history_item,
)
from app.core.source_trust_rules import (
    is_source_trusted_for_auto,
)
from app.core.auto_review_panel import (
    save_auto_review_item,
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
        post_text = render_earthquake_signal(signal)
        validation = validate_editor_draft(post_text)

        warnings_text = "\n".join(
            f"- {w.get('severity')}: {w.get('type')} — {w.get('message', '')}"
            for w in validation.get("warnings", [])
        )

        if not warnings_text:
            warnings_text = "none"
        message = (
            "📰 SIGNAL PREVIEW\n\n"
            f"SOURCE: {status.get('source_used')}\n"
            f"SCORE: {validation.get('score')}\n"
            f"RISK: {validation.get('editorial_risk')}\n\n"
            "━━━━━━━━━━\n\n"
            "AI DRAFT:\n\n"
            f"{post_text}\n\n"
            "━━━━━━━━━━\n\n"
            "WARNINGS:\n\n"
            f"{warnings_text}"
        )

        preview = build_preview_item(
            signal,
            message,
        )

        print_preview_item(preview)
        add_pending_preview(
            signal["signal_id"],
            message,
            signal,
        )

        auto_result = should_auto_approve(signal)

        print("=== AUTO APPROVAL CHECK ===")
        print("SIGNAL:", signal["signal_id"])
        print("APPROVED:", auto_result["approved"])
        print("REASON:", auto_result["reason"])
        print("=== END AUTO APPROVAL CHECK ===")
        save_auto_approval_audit(
            signal["signal_id"],
            auto_result,
            signal,
        )

        if auto_result["approved"]:
            print("=== AUTO APPROVAL ROUTING ===")
            print("MODE: REAL_AUTO_PUBLISH")
            print("ACTION: AUTO_PUBLISH")
            print("SIGNAL:", signal["signal_id"])
            print("REASON:", auto_result["reason"])
            print("=== END AUTO APPROVAL ROUTING ===")
            if is_cooldown_triggered():
                print("AUTO COOLDOWN ACTIVE")
                print("ACTION: FALLBACK_TO_MANUAL")
                save_auto_review_item(
                    signal["signal_id"],
                    "auto_cooldown_active",
                    status.get("source_used") or "unknown",
                )
                send_admin_preview(
                    signal["signal_id"],
                    message,
                )

                continue
            if is_cluster_blocked(signal):
                print("ANTI SPAM CLUSTER ACTIVE")
                print("ACTION: FALLBACK_TO_MANUAL")
                save_auto_review_item(
                    signal["signal_id"],
                    "anti_spam_cluster_active",
                    status.get("source_used") or "unknown",
                )
                send_admin_preview(
                    signal["signal_id"],
                    message,
                )

                continue
            if is_rate_limit_triggered():
                print("AUTO RATE LIMIT ACTIVE")
                print("ACTION: FALLBACK_TO_MANUAL")
                save_auto_review_item(
                    signal["signal_id"],
                    "auto_rate_limit_active",
                    status.get("source_used") or "unknown",
                )
                send_admin_preview(
                    signal["signal_id"],
                    message,
                )

                continue
            if not is_source_trusted_for_auto(signal):
                print("SOURCE TRUST BLOCKED")
                print("ACTION: FALLBACK_TO_MANUAL")
                print(
                    "SOURCE:",
                    signal.get("source")
                    or signal.get("source_name")
                    or "unknown",
                )
                save_auto_review_item(
                    signal["signal_id"],
                    "source_trust_blocked",
                    status.get("source_used") or "unknown",
                )
                send_admin_preview(
                    signal["signal_id"],
                    message,
                )

                continue
            from app.core.post_cleaner import extract_public_post
            from app.core.channel_publisher import publish_to_channel
            if was_auto_published(signal["signal_id"]):
                print("AUTO DUPLICATE SKIPPED:", signal["signal_id"])
                continue
            public_post = extract_public_post(message)

            publish_to_channel(public_post)

            save_auto_published(
                signal["signal_id"],
                auto_result["reason"],
            )

            save_auto_publish_timestamp()
            save_cluster_history_item(signal)
        else:
            print("=== AUTO APPROVAL ROUTING ===")
            print("MODE: MANUAL_REVIEW")
            print("ACTION: SEND_TO_PREVIEW")
            print("SIGNAL:", signal["signal_id"])
            print("REASON:", auto_result["reason"])
            print("=== END AUTO APPROVAL ROUTING ===")
            save_auto_review_item(
                signal["signal_id"],
                auto_result["reason"],
                status.get("source_used") or "unknown",
            )
            send_admin_preview(
                signal["signal_id"],
                message,
            )

    status["result"] = "ok_ready_to_publish"
    save_pipeline_status(status)

    return health
if __name__ == "__main__":
    run_pipeline({})