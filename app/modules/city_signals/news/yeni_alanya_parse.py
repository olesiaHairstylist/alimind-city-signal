import xml.etree.ElementTree as ET
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[3]

RAW_DIR = (
    BASE_DIR / "data" / "raw" / "news" / "yeni_alanya"
)


def get_latest_raw_file() -> Path | None:
    if not RAW_DIR.exists():
        return None

    files = sorted(RAW_DIR.glob("*.xml"))

    if not files:
        return None

    return files[-1]


def parse_yeni_alanya_rss(raw_text: str) -> list:
    root = ET.fromstring(raw_text)

    items = []

    for item in root.findall(".//item"):
        title = item.findtext("title", default="").strip()
        link = item.findtext("link", default="").strip()
        pub_date = item.findtext("pubDate", default="").strip()
        description = item.findtext("description", default="").strip()
        enclosure = item.find("enclosure")

        image_url = ""

        if enclosure is not None:
            image_url = enclosure.get("url", "").strip()
        items.append(
            {
                "title": title,
                "link": link,
                "pubDate": pub_date,
                "description": description,
                "image_url": image_url,
            }

        )

    return items


if __name__ == "__main__":
    raw_file = get_latest_raw_file()

    if raw_file is None:
        print("NO RAW FILE")
    else:
        print("RAW FILE:", raw_file)

        raw_text = raw_file.read_text(encoding="utf-8")

        items = parse_yeni_alanya_rss(raw_text)

        print("PARSED ITEMS:", len(items))

        for item in items[:5]:
            print("----")
            print("TITLE:", item["title"])
            print("DATE:", item["pubDate"])
            print("LINK:", item["link"])
            print("IMAGE:", item["image_url"])