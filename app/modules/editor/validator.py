FORBIDDEN_WORDS = [
    "катастрофа",
    "ужас",
    "шок",
    "апокалипсис",
    "все погибнут",
    "срочно",
]

SUSPICIOUS_FILLERS = [
    "причины уточняются",
    "подробности уточняются",
    "обстоятельства выясняются",
    "информация уточняется",
    "данные уточняются",
]


def validate_editor_draft(text: str) -> dict:
    errors = []
    warnings = []


    if not text.strip():
        errors.append({
            "type": "empty_text",
            "severity": "high",
            "message": "AI вернул пустой текст"
        })
    if len(text) < 80:
        warnings.append({
            "type": "too_short",
            "severity": "low",
            "message": "Текст получился слишком коротким"
        })



    lower_text = text.lower()

    for word in FORBIDDEN_WORDS:
        lower_text = text.lower()

        for filler in SUSPICIOUS_FILLERS:
            if filler in lower_text:
                warnings.append({
                    "type": "suspicious_filler",
                    "severity": "medium",
                    "message": "AI добавил фразу, которой нет в raw signal"
                })

    for filler in SUSPICIOUS_FILLERS:
        if filler in lower_text:
            warnings.append({
                "type": "suspicious_filler",
                "severity": "medium"
            })
    score = 100

    score -= len(errors) * 30
    score -= len(warnings) * 10

    if score < 0:
        score = 0
    if score >= 90:
        editorial_risk = "low"

    elif score >= 70:
        editorial_risk = "medium"

    else:
        editorial_risk = "high"
    return {
        "ok": len(errors) == 0,
        "warnings": warnings,
        "errors": errors,
        "score": score,
        "editorial_risk": editorial_risk,
    }

