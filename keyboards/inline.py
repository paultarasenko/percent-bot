"""
Post-result keyboard shown after every successful calculation.
"""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from texts.messages import BTN_NEW_CALC, BTN_MAIN_MENU, BTN_FORMULA

CB_NEW_CALC = "action:new_calc"
CB_MAIN_MENU = "action:main_menu"
CB_FORMULA = "action:formula"


def after_result_keyboard(show_formula: bool = False) -> InlineKeyboardMarkup:
    """Keyboard shown right after a calculation result."""
    rows = []
    if show_formula:
        rows.append([InlineKeyboardButton(text=BTN_FORMULA, callback_data=CB_FORMULA)])
    rows.append([
        InlineKeyboardButton(text=BTN_NEW_CALC, callback_data=CB_NEW_CALC),
        InlineKeyboardButton(text=BTN_MAIN_MENU, callback_data=CB_MAIN_MENU),
    ])
    return InlineKeyboardMarkup(inline_keyboard=rows)
