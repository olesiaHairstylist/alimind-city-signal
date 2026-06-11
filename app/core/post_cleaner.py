def extract_public_post(preview_text: str) -> str:
    marker = "AI DRAFT:"

    if marker not in preview_text:
        return preview_text

    text = preview_text.split(marker, 1)[1]

    if "━━━━━━━━━━" in text:
        text = text.split("━━━━━━━━━━", 1)[0]

    return text.strip()