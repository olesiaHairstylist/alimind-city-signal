def should_auto_approve(signal: dict):
    magnitude = signal.get("magnitude", 0)

    if magnitude < 3.0:
        return {
            "approved": True,
            "reason": "magnitude_below_3"
        }

    return {
        "approved": False,
        "reason": "rules_not_matched"
    }