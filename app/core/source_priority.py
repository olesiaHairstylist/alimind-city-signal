def calculate_source_score(info: dict) -> int:
    score = 100

    if not info.get("alive"):
        score -= 40

    if info.get("stale"):
        score -= 30

    failures = info.get("consecutive_failures", 0)

    score -= failures * 10

    return max(score, 0)


def choose_best_source(health: dict):
    sources = health.get("sources", {})

    if not sources:
        return None

    ranked = []

    for source_id, info in sources.items():
        score = calculate_source_score(info)

        ranked.append(
            (score, source_id)
        )

    ranked.sort(reverse=True)

    best_score, best_source = ranked[0]

    return {
        "source": best_source,
        "score": best_score,
        "ranking": ranked,
    }