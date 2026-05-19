import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]

REGISTRY_PATH = (
    BASE_DIR
    / "data"
    / "sources"
    / "source_registry.json"
)


def load_sources():
    with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def get_source(source_id: str):
    sources = load_sources()

    for source in sources:
        if source.get("id") == source_id:
            return source

    return None