from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

def create_inline_kb(width: int, buttons_dict: dict) -> InlineKeyboardMarkup:
    
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []

    for button, text in buttons_dict.items():
        buttons.append(InlineKeyboardButton(
            text=text,
            callback_data=button))

    kb_builder.row(*buttons, width=width)

    return kb_builder.as_markup()
