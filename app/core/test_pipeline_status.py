from app.core.pipeline_status import (
    save_pipeline_status,
    load_pipeline_status,
)


def main():
    status = {
        "pipeline": "earthquake",
        "primary_source": "koeri",
        "fallback_used": True,
        "events_count": 6,
        "filtered_count": 0,
        "new_signals_count": 0,
        "result": "ok",
    }

    save_pipeline_status(status)

    loaded = load_pipeline_status()

    print("STATUS:")
    print(loaded)

    print("PIPELINE_STATUS_V1 OK")


if __name__ == "__main__":
    main()