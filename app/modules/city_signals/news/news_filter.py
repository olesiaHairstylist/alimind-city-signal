ALANYA_KEYWORDS = [
    "alanya",
    "alanya'da",
    "alanya’da",
    "alanya'ya",
    "alanya’ya",
    "alanyada",
]


def is_alanya_news(signal: dict) -> bool:
    title = signal.get("title", "").lower()
    description = signal.get("description", "").lower()

    text = f"{title} {description}"

    return any(keyword in text for keyword in ALANYA_KEYWORDS)