from app.modules.city_signals.news.yeni_alanya_parse import (
    get_latest_raw_file,
    parse_yeni_alanya_rss,
)
import hashlib

def normalize_yeni_alanya_items(items: list) -> list:
    signals = []

    for item in items:
        title = item.get("title", "").strip()
        link = item.get("link", "").strip()
        published_at = item.get("pubDate", "").strip()

        if not title or not link:
            continue

        signals.append(
            {
                "signal_id": hashlib.md5(
                    link.encode("utf-8")
                ).hexdigest()[:16],
                "source": "yeni_alanya",
                "category": "news",
                "location": "alanya",
                "title": title,
                "link": link,
                "published_at": published_at,
                "description": item.get("description", "").strip(),
                "image_url": item.get("image_url", "").strip(),
            }

        )

    return signals


if __name__ == "__main__":
    raw_file = get_latest_raw_file()

    if raw_file is None:
        print("NO RAW FILE")
    else:
        raw_text = raw_file.read_text(encoding="utf-8")

        items = parse_yeni_alanya_rss(raw_text)
        signals = normalize_yeni_alanya_items(items)

        print("NORMALIZED NEWS SIGNALS:", len(signals))

        for signal in signals[:5]:
            print("----")
            print("ID:", signal["signal_id"])
            print("SOURCE:", signal["source"])
            print("CATEGORY:", signal["category"])
            print("LOCATION:", signal["location"])
            print("TITLE:", signal["title"])
            print("DATE:", signal["published_at"])
            print("LINK:", signal["link"])
            print("DESCRIPTION:", signal["description"])
            print("IMAGE:", signal["image_url"])