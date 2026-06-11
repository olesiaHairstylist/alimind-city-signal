def validate_signal_quality(raw_message: str) -> dict:
    errors = []

    lower = raw_message.lower()

    if "location unavailable" in lower:
        errors.append("missing_location")

    if "time unavailable" in lower:
        errors.append("missing_time")

    if "m ?" in lower:
        errors.append("missing_magnitude")

    return {
        "ok": len(errors) == 0,
        "errors": errors,
    }