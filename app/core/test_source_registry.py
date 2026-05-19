from app.core.source_registry import (
    load_sources,
    get_source,
)


def main():
    sources = load_sources()

    print("SOURCES COUNT:", len(sources))

    koeri = get_source("koeri")

    print("KOERI:", koeri)

    if not koeri:
        raise RuntimeError(
            "KOERI source not found"
        )

    print("SOURCE_REGISTRY_V1 OK")


if __name__ == "__main__":
    main()