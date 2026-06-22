import os

from dotenv import load_dotenv
from openai import OpenAI

from app.modules.editor.prompt import SYSTEM_PROMPT
from app.modules.editor.style_prompt import STYLE_PROMPT

from app.modules.editor.signal_quality import EDITOR_RULES
from app.modules.editor.context_rules import get_context_rules
load_dotenv(override=True)


def build_editor_prompt(raw_message: str) -> str:
    context_rules = get_context_rules(raw_message)

    return f"""
{SYSTEM_PROMPT}

{EDITOR_RULES}

{STYLE_PROMPT}

{context_rules}

RAW SIGNAL:

{raw_message}

Сделай короткую новость на русском языке для русскоязычных жителей Аланьи.
Используй только факты из источника.
Не придумывай детали.
"""


def generate_editor_draft(raw_message: str) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    model = os.getenv("OPENAI_MODEL", "gpt-5.5-mini")

    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not found")

    client = OpenAI(api_key=api_key)

    response = client.responses.create(
        model=model,
        input=build_editor_prompt(raw_message),
    )

    return response.output_text.strip()