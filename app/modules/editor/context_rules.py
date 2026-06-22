CONTEXT_RULES = {
    "power": [
        "Что отключают?",
        "Когда?",
        "Во сколько?",
        "Какие махалле?",
        "Сколько продлятся работы?",
    ],
    "accident": [
        "Что случилось?",
        "Где?",
        "Почему?",
        "Кто участвовал?",
        "Какой итог?",
    ],
    "real_estate": [
        "Что изменилось?",
        "Какие цифры?",
        "Какие районы?",
        "За какой период?",
        "Почему это важно?",
    ],
    "government": [
        "Что решили?",
        "Когда вступает?",
        "Кого касается?",
        "Что изменится?",
    ],
    "tourism": [
        "Что произошло?",
        "Где?",
        "Кого касается?",
        "Есть последствия?",
    ],
}
CONTEXT_KEYWORDS = {
    "power": [
        "elektrik",
        "kesinti",
        "su kesintisi",
        "вода",
        "электричество",
        "отключ",
        "свет",
    ],
    "accident": [
        "kaza",
        "trafik",
        "polis",
        "yakalandı",
        "ceza",
        "штраф",
        "дтп",
        "авар",
        "полиция",
        "задерж",
        "погон",
    ],
    "real_estate": [
        "konut",
        "arsa",
        "emlak",
        "gayrimenkul",
        "цены на жиль",
        "недвиж",
        "земл",
        "квартир",
    ],
    "government": [
        "belediye",
        "kaymakam",
        "bakan",
        "karar",
        "yasa",
        "закон",
        "муниципал",
        "решен",
        "власти",
    ],
    "tourism": [
        "turist",
        "otel",
        "plaj",
        "turizm",
        "турист",
        "отель",
        "пляж",
    ],
}


def detect_context(raw_message: str) -> str:
    text = raw_message.lower()

    for context, keywords in CONTEXT_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text:
                return context

    return "general"


def get_context_rules(raw_message: str) -> str:
    context = detect_context(raw_message)

    questions = CONTEXT_RULES.get(context)

    if not questions:
        return """
Общие вопросы:
- Что произошло?
- Где произошло?
- Когда произошло?
- Кого это касается?
- Что это значит для жителей Аланьи?
"""

    lines = [f"Тип новости: {context}", "", "Ответь на вопросы:"]
    for question in questions:
        lines.append(f"- {question}")

    return "\n".join(lines)