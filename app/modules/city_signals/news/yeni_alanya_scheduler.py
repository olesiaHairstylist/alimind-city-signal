import time

from app.modules.city_signals.news.yeni_alanya_pipeline import (
    run_yeni_alanya_pipeline,
)

SLEEP_SECONDS = 300


def run_scheduler():
    while True:
        try:
            run_yeni_alanya_pipeline()

        except Exception as e:
            print("YENI ALANYA SCHEDULER ERROR:", e)

        print(f"SLEEP {SLEEP_SECONDS} sec...")
        time.sleep(SLEEP_SECONDS)


if __name__ == "__main__":
    run_scheduler()