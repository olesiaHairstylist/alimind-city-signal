from app.core.pipeline_status import (
    load_pipeline_status,
)


def render_pipeline_status() -> str:
    status = load_pipeline_status()

    lines = [
        "=== PIPELINE STATUS ===",
        f"pipeline: {status.get('pipeline')}",
        f"primary_source: {status.get('primary_source')}",
        f"source_used: {status.get('source_used')}",
        f"fallback_used: {status.get('fallback_used')}",
        f"events_count: {status.get('events_count')}",
        f"filtered_count: {status.get('filtered_count')}",
        f"normalized_count: {status.get('normalized_count')}",
        f"new_signals_count: {status.get('new_signals_count')}",
        f"result: {status.get('result')}",
        f"updated_at: {status.get('updated_at')}",
    ]

    return "\n".join(lines)