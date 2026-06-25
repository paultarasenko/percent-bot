"""
Main menu keyboard — mode selection.
"""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from texts.messages import (
    MODE_PERCENT_OF,
    MODE_WHAT_PERCENT,
    MODE_CHANGE,
    MODE_LOAN,
    MODE_DEPOSIT,
)

CB_PERCENT_OF = "mode:percent_of"
CB_WHAT_PERCENT = "mode:what_percent"
CB_CHANGE = "mode:change"
CB_LOAN = "mode:loan"
CB_DEPOSIT = "mode:deposit"


def main_menu_keyboard() -> InlineKeyboardMarkup:
    """Build and return the main menu inline keyboard."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=MODE_PERCENT_OF, callback_data=CB_PERCENT_OF)],
            [InlineKeyboardButton(text=MODE_WHAT_PERCENT, callback_data=CB_WHAT_PERCENT)],
            [InlineKeyboardButton(text=MODE_CHANGE, callback_data=CB_CHANGE)],
            [InlineKeyboardButton(text=MODE_LOAN, callback_data=CB_LOAN)],
            [InlineKeyboardButton(text=MODE_DEPOSIT, callback_data=CB_DEPOSIT)],
        ]
    )
