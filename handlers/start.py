"""
Entry point handlers: /start command and main menu navigation callbacks.
"""
import logging

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from keyboards import main_menu_keyboard, CB_NEW_CALC, CB_MAIN_MENU
from texts.messages import WELCOME

logger = logging.getLogger(__name__)
router = Router(name="start")


async def _show_main_menu(target: Message, state: FSMContext) -> None:
    """Clear FSM state and send the main menu."""
    await state.clear()
    await target.answer(
        text=WELCOME,
        reply_markup=main_menu_keyboard(),
        parse_mode="HTML",
    )


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext) -> None:
    """Handle /start command."""
    logger.info("User %s started the bot", message.from_user.id if message.from_user else "unknown")
    await _show_main_menu(message, state)


@router.callback_query(lambda c: c.data == CB_MAIN_MENU)
async def cb_main_menu(callback: CallbackQuery, state: FSMContext) -> None:
    """Return to main menu from anywhere."""
    await callback.answer()
    await state.clear()
    await callback.message.answer(  # type: ignore[union-attr]
        text=WELCOME,
        reply_markup=main_menu_keyboard(),
        parse_mode="HTML",
    )


@router.callback_query(lambda c: c.data == CB_NEW_CALC)
async def cb_new_calc(callback: CallbackQuery, state: FSMContext) -> None:
    """'New calculation' — go back to main menu and pick a mode."""
    await callback.answer()
    await state.clear()
    await callback.message.answer(  # type: ignore[union-attr]
        text=WELCOME,
        reply_markup=main_menu_keyboard(),
        parse_mode="HTML",
    )
