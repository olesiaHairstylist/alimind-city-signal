from aiogram import Router, F
from aiogram.types import CallbackQuery

from app.modules.moderation.handler import (
    handle_moderation_callback,
)

router = Router()


@router.callback_query(F.data.startswith("mod:"))
async def moderation_callback(callback: CallbackQuery):
    data = callback.data or ""

    print("CALLBACK DATA:", data)

    result = handle_moderation_callback(data)

    try:
        await callback.answer(result)
    except Exception as e:
        print("CALLBACK ANSWER FAILED:", e)

    old_text = callback.message.text or ""

    new_text = f"{result}\n\n{old_text}"

    if new_text != old_text:
        try:
            await callback.message.edit_text(new_text)
        except Exception as e:
            print("CALLBACK EDIT FAILED:", e)