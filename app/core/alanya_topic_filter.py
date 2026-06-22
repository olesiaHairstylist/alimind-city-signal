ALANYA_KEYWORDS = [
    "alanya",
    "mahmutlar",
    "oba",
    "kestel",
    "tosmur",
    "konaklı",
    "konakli",
    "avsallar",
    "gazipaşa",
    "gazipasa",
    "demirtaş",
    "demirtas",
    "payallar",
    "türkler",
    "turkler",
    "okurcalar",
    "inçekum",
    "incekum",
    "dinek",
    "cleopatra",
    "kleopatra",
]

BLOCKED_KEYWORDS = [
    "beşiktaş",
    "besiktas",
    "galatasaray",
    "fenerbahçe",
    "fenerbahce",
    "trabzonspor",
    "basketbol",
    "futbol",
    "voleybol",
    "spor",
    "maç",
    "mac",
    "final",
    "şampiyon",
    "sampiyon",
]


def normalize_text(value: str) -> str:
    if not value:
        return ""

    return value.lower().strip()


def is_alanya_related(signal: dict) -> bool:
    title = normalize_text(signal.get("title"))
    link = normalize_text(signal.get("link"))
    text = f"{title} {link}"

    return any(keyword in text for keyword in ALANYA_KEYWORDS)


def is_blocked_topic(signal: dict) -> bool:
    title = normalize_text(signal.get("title"))

    return any(keyword in title for keyword in BLOCKED_KEYWORDS)


def should_process_alanya_news(signal: dict) -> bool:
    if not is_alanya_related(signal):
        return False

    if is_blocked_topic(signal):
        return False

    return True