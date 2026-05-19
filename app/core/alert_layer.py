def build_alerts(health: dict) -> list[str]:
    alerts = []

    sources = health.get("sources", {})

    if not sources:
        alerts.append("NO_SOURCES_IN_HEALTH")
        return alerts

    dead_sources = []

    for source_id, info in sources.items():
        if not info.get("alive"):
            dead_sources.append(source_id)

        if info.get("consecutive_failures", 0) >= 3:
            alerts.append(
                f"SOURCE_REPEATED_FAILURES: {source_id} "
                f"failures={info.get('consecutive_failures')}"
            )

    if len(dead_sources) == len(sources):
        alerts.append(
            "ALL_SOURCES_DEAD: " + ", ".join(dead_sources)
        )

    return alerts


def print_alerts(alerts: list[str]) -> None:
    print("\n=== ALERT LAYER ===")

    if not alerts:
        print("NO ALERTS")
        return

    for alert in alerts:
        print("ALERT:", alert)