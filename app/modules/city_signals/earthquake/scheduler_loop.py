import time
from datetime import datetime, UTC

from app.modules.city_signals.earthquake.pipeline_runner import (
    run_pipeline,
)


INTERVAL_SECONDS = 180


def main():
    print("SCHEDULER_LOOP_V1 STARTED")
    health = {}
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
            print(
                source_id,
                "| alive =", info.get("alive"),
                "| failures =", info.get("consecutive_failures"),
                "| last_success =", info.get("last_success_at"),
            )
        print(
            f"\nSLEEP {INTERVAL_SECONDS} sec...\n"
        )

        time.sleep(INTERVAL_SECONDS)


if __name__ == "__main__":
    main()
