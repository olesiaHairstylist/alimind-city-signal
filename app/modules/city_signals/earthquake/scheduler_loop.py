import time
from datetime import datetime, UTC
from app.core.stale_detection import is_stale_iso
from app.core.source_priority import choose_best_source
from app.core.control_state import (
    load_control_state,
    save_control_state,
)
from app.core.alert_layer import (
    build_alerts,
    print_alerts,
)
from app.modules.city_signals.earthquake.pipeline_runner import (
    run_pipeline,
)


INTERVAL_SECONDS = 180


def main():
    print("SCHEDULER_LOOP_V1 STARTED")
    health = load_control_state()
    while True:
        started_at = datetime.now(UTC)

        print("\n====================")
        print(
            "PIPELINE START:",
            started_at.isoformat(),
        )
        print("====================\n")

        try:
            health = run_pipeline(health)

        except Exception as e:
            print("PIPELINE CRASH:", e)
        print("\n=== HEALTH STATUS ===")

        for source_id, info in health.get("sources", {}).items():
            is_stale = is_stale_iso(
                info.get("last_success_at"),
                max_age_seconds=300,
            )
            print(
                source_id,
                "| alive =", info.get("alive"),
                "| stale =", is_stale,
                "| failures =", info.get("consecutive_failures"),
                "| last_success =", info.get("last_success_at"),
            )

        priority = choose_best_source(health)

        print("\n=== SOURCE PRIORITY ===")

        if priority:
            print(
                "BEST:",
                priority["source"],
                "| score =",
                priority["score"],
            )

            print("RANKING:")

            for score, source_id in priority["ranking"]:
                print(
                    source_id,
                    "=>",
                    score,
                )
        save_control_state(health)
        alerts = build_alerts(health)
        print_alerts(alerts)

        print(

            f"\nSLEEP {INTERVAL_SECONDS} sec...\n"
        )

        time.sleep(INTERVAL_SECONDS)


if __name__ == "__main__":
    main()