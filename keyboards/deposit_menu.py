"""
Deposit type selection keyboard.
"""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from texts.messages import MODE_DEPOSIT_SIMPLE, MODE_DEPOSIT_COMPOUND

CB_DEPOSIT_SIMPLE = "mode:deposit_simple"
CB_DEPOSIT_COMPOUND = "mode:deposit_compound"


def deposit_menu_keyboard() -> InlineKeyboardMarkup:
    """Choose between simple and compound deposit."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=MODE_DEPOSIT_SIMPLE, callback_data=CB_DEPOSIT_SIMPLE)],
            [InlineKeyboardButton(text=MODE_DEPOSIT_COMPOUND, callback_data=CB_DEPOSIT_COMPOUND)],
        ]
    )
