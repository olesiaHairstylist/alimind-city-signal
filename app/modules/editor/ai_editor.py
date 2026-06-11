import os

from dotenv import load_dotenv
from openai import OpenAI

from app.modules.editor.prompt import SYSTEM_PROMPT
from app.modules.editor.style_prompt import STYLE_PROMPT

load_dotenv(override=True)

def build_editor_prompt(raw_message: str) -> str:
    return f"""
{STYLE_PROMPT}

RAW SIGNAL:

{raw_message}

Сделай короткую новость на русском языке.
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