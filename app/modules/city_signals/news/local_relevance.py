ALANYA_KEYWORDS = [
    "alanya",
    "аланья",
    "mahmutlar",
    "oba",
    "tosmur",
    "kestel",
    "avsallar",
    "konakli",
    "payallar",
    "okurcalar",
    "demirtas",
    "gazipasa",
    "altso",
    "alkü",
    "belediyesi",
]


def is_locally_relevant(signal: dict) -> bool:
    text = (
        signal.get("title", "") + " " +
        signal.get("description", "")
    ).lower()

    return any(keyword in text for keyword in ALANYA_KEYWORDS)