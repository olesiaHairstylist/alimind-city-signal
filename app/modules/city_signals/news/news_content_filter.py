BLOCK_WORDS = [
    "cinayet",
    "öldürüldü",
    "öldürdü",
    "intihar",
    "ceset",
    "cansız bedeni",
    "uyuşturucu",
    "mahkeme",
    "tutuklandı",
    "gözaltına alındı",
    "bıçaklandı",
    "silahla",
    "dolandırıcılık",
    "kumar",
    "bahis",
]


def is_blocked_news(signal: dict) -> bool:
    text = (
        signal.get("title", "")
        + " "
        + signal.get("description", "")
    ).lower()

    for word in BLOCK_WORDS:
        if word in text:
            return True

    return False