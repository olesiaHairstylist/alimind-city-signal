from app.modules.city_signals.news.yeni_alanya_fetch import (
    fetch_yeni_alanya,
    save_raw_yeni_alanya,
)

from app.modules.city_signals.news.yeni_alanya_parse import (
    parse_yeni_alanya_rss,
)

from app.modules.city_signals.news.yeni_alanya_normalize import (
    normalize_yeni_alanya_items,
)

from app.modules.city_signals.news.yeni_alanya_preview import (
    render_news_preview,
)

from app.modules.city_signals.news.news_dedup import (
    filter_new_news,
    save_seen_news,
)
from app.modules.city_signals.news.news_filter import (
    is_alanya_news,
)

from app.modules.city_signals.news.news_moderation_message import (
    render_news_moderation_message,
)

from app.core.channel_publisher import (
    publish_to_channel,
    publish_photo_to_channel,
)
from app.modules.editor.ai_editor import generate_editor_draft
from app.modules.city_signals.news.news_content_filter import (
    is_blocked_news,
)
from app.core.preview_sender import (
    send_preview_message,
)
from app.core.publish_decisions import (
    add_pending_preview,
)

def run_yeni_alanya_pipeline():
    print("=== YENI ALANYA NEWS PIPELINE ===")

    raw = fetch_yeni_alanya()

    if raw is None:
        print("NO RAW DATA")
        return

    raw_path = save_raw_yeni_alanya(raw)
    print("RAW SAVED:", raw_path)

    items = parse_yeni_alanya_rss(raw)
    print("PARSED ITEMS:", len(items))

    signals = normalize_yeni_alanya_items(items)
    print("NORMALIZED SIGNALS:", len(signals))

    new_signals = filter_new_news(signals)
    print("NEW NEWS:", len(new_signals))

    if not new_signals:
        print("NO NEW NEWS")
        return

    for signal in new_signals:
        print("----")
        print(render_news_preview(signal))

        if is_alanya_news(signal):
            if is_blocked_news(signal):
                print("NEWS BLOCKED BY CONTENT FILTER")
                save_seen_news(signal["signal_id"])
                continue
            raw_news = f"""
        SOURCE:
        Yeni Alanya

        TITLE:
        {signal.get("title")}

        DESCRIPTION:
        {signal.get("description")}

        LINK:
        {signal.get("link")}
        """

            message = generate_editor_draft(raw_news)

            if "Источник:" not in message:
                message = message + f"\n\nИсточник: Yeni Alanya\n{signal.get('link')}"

            message += "\n\n#Алания #НовостиАлании #Alanya #Турция"

            image_url = signal.get("image_url", "")
            add_pending_preview(
                signal["signal_id"],
                message,
                signal,
            )
            preview_result = send_preview_message(
                signal["signal_id"],
                message,
            )

            print("PREVIEW RESULT:", preview_result)
            print("NEWS SENT TO PREVIEW")
            print("NEWS SENT TO PREVIEW")

            print("NEWS SENT TO MODERATION")

        else:
            print("NEWS SKIPPED: NOT ALANYA")

        save_seen_news(signal["signal_id"])
    print("=== END YENI ALANYA NEWS PIPELINE ===")


if __name__ == "__main__":
    run_yeni_alanya_pipeline()