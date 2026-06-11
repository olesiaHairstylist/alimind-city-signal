from app.modules.city_signals.news.yeni_alanya_parse import (
    get_latest_raw_file,
    parse_yeni_alanya_rss,
)

from app.modules.city_signals.news.yeni_alanya_normalize import (
    normalize_yeni_alanya_items,
)


def render_news_preview(signal: dict) -> str:
    return (
        "📰 NEWS PREVIEW\n\n"
        f"SOURCE: {signal.get('source')}\n"
        f"CATEGORY: {signal.get('category')}\n"
        f"LOCATION: {signal.get('location')}\n\n"
        "━━━━━━━━━━\n\n"
        f"TITLE:\n{signal.get('title')}\n\n"
        f"DATE:\n{signal.get('published_at')}\n\n"
        f"LINK:\n{signal.get('link')}\n"
    )


if __name__ == "__main__":
    raw_file = get_latest_raw_file()

    if raw_file is None:
        print("NO RAW FILE")
    else:
        raw_text = raw_file.read_text(encoding="utf-8")

        items = parse_yeni_alanya_rss(raw_text)
        signals = normalize_yeni_alanya_items(items)

        print("NEWS PREVIEWS:", len(signals))

        for signal in signals[:3]:
            print("----")
            print(render_news_preview(signal))