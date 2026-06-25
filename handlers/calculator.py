"""
Calculator handlers — one FSM flow per calculation mode.
"""
import logging

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from keyboards import (
    after_result_keyboard,
    deposit_menu_keyboard,
    CB_CHANGE,
    CB_LOAN,
    CB_PERCENT_OF,
    CB_WHAT_PERCENT,
    CB_DEPOSIT,
    CB_DEPOSIT_SIMPLE,
    CB_DEPOSIT_COMPOUND,
    CB_FORMULA,
)
from services.calculator import (
    loan_annuity,
    percent_change,
    percent_of,
    what_percent,
    deposit_simple,
    deposit_compound,
)
from states import (
    ChangeStates,
    LoanStates,
    PercentOfStates,
    WhatPercentStates,
    DepositStates,
    DepositCompoundStates,
)
from texts.messages import (
    ASK_FROM,
    ASK_LOAN_AMOUNT,
    ASK_LOAN_MONTHS,
    ASK_LOAN_RATE,
    ASK_NUMBER,
    ASK_PART,
    ASK_PERCENT,
    ASK_TO,
    ASK_WHOLE,
    ASK_DEPOSIT_AMOUNT,
    ASK_DEPOSIT_RATE,
    ASK_DEPOSIT_MONTHS,
    RESULT_CHANGE,
    RESULT_LOAN,
    RESULT_PERCENT_OF,
    RESULT_WHAT_PERCENT,
    RESULT_DEPOSIT,
    RESULT_DEPOSIT_COMPOUND,
)
from utils.formatters import fmt_input, fmt_number
from utils.validators import (
    ValidationError,
    parse_float,
    parse_nonzero_float,
    parse_positive_float,
    parse_steps,
)

logger = logging.getLogger(__name__)
router = Router(name="calculator")


# ── Helpers ───────────────────────────────────────────────────────────────────

async def _ask(message: Message, prompt: str) -> None:
    await message.answer(prompt, parse_mode="HTML")


async def _send_result(message: Message, state: FSMContext, text: str, show_formula: bool = False) -> None:
    await state.clear()
    await message.answer(
        text=text,
        parse_mode="HTML",
        reply_markup=after_result_keyboard(show_formula=show_formula),
    )


async def _handle_validation_error(message: Message, exc: ValidationError) -> None:
    await message.answer(exc.message, parse_mode="HTML")


@router.callback_query(lambda c: c.data == CB_FORMULA)
async def cb_formula(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    data = await state.get_data()
    formula = data.get("formula", "")
    if formula:
        await callback.message.answer(formula, parse_mode="HTML")  # type: ignore[union-attr]


# ════════════════════════════════════════════════════════════════════════════
# MODE 1 — % от числа
# ════════════════════════════════════════════════════════════════════════════

@router.callback_query(lambda c: c.data == CB_PERCENT_OF)
async def start_percent_of(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    await state.set_state(PercentOfStates.waiting_percent)
    await callback.message.answer(ASK_PERCENT, parse_mode="HTML")  # type: ignore[union-attr]


@router.message(PercentOfStates.waiting_percent)
async def got_percent_for_percent_of(message: Message, state: FSMContext) -> None:
    try:
        percent = parse_float(message.text or "")
    except ValidationError as exc:
        await _handle_validation_error(message, exc)
        return
    await state.update_data(percent=percent)
    await state.set_state(PercentOfStates.waiting_number)
    await _ask(message, ASK_NUMBER)


@router.message(PercentOfStates.waiting_number)
async def got_number_for_percent_of(message: Message, state: FSMContext) -> None:
    try:
        number = parse_float(message.text or "")
    except ValidationError as exc:
        await _handle_validation_error(message, exc)
        return
    data = await state.get_data()
    percent: float = data["percent"]
    result = percent_of(percent, number)
    text = RESULT_PERCENT_OF.format(
        percent=fmt_input(percent),
        number=fmt_input(number),
        result=fmt_number(result.value),
    )
    await _send_result(message, state, text)


# ════════════════════════════════════════════════════════════════════════════
# MODE 2 — Найти процент
# ════════════════════════════════════════════════════════════════════════════

@router.callback_query(lambda c: c.data == CB_WHAT_PERCENT)
async def start_what_percent(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    await state.set_state(WhatPercentStates.waiting_whole)
    await callback.message.answer(ASK_WHOLE, parse_mode="HTML")  # type: ignore[union-attr]


@router.message(WhatPercentStates.waiting_whole)
async def got_whole(message: Message, state: FSMContext) -> None:
    try:
        whole = parse_nonzero_float(message.text or "")
    except ValidationError as exc:
        await _handle_validation_error(message, exc)
        return
    await state.update_data(whole=whole)
    await state.set_state(WhatPercentStates.waiting_part)
    await _ask(message, ASK_PART)


@router.message(WhatPercentStates.waiting_part)
async def got_part(message: Message, state: FSMContext) -> None:
    try:
        part = parse_float(message.text or "")
    except ValidationError as exc:
        await _handle_validation_error(message, exc)
        return
    data = await state.get_data()
    whole: float = data["whole"]
    result = what_percent(part, whole)
    text = RESULT_WHAT_PERCENT.format(
        part=fmt_input(part),
        whole=fmt_input(whole),
        result=fmt_number(result.value),
    )
    await _send_result(message, state, text)


# ════════════════════════════════════════════════════════════════════════════
# MODE 3 — Изменение в %
# ════════════════════════════════════════════════════════════════════════════

@router.callback_query(lambda c: c.data == CB_CHANGE)
async def start_change(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    await state.set_state(ChangeStates.waiting_from)
    await callback.message.answer(ASK_FROM, parse_mode="HTML")  # type: ignore[union-attr]


@router.message(ChangeStates.waiting_from)
async def got_from(message: Message, state: FSMContext) -> None:
    try:
        from_val = parse_nonzero_float(message.text or "")
    except ValidationError as exc:
        await _handle_validation_error(message, exc)
        return
    await state.update_data(from_val=from_val)
    await state.set_state(ChangeStates.waiting_to)
    await _ask(message, ASK_TO)


@router.message(ChangeStates.waiting_to)
async def got_to(message: Message, state: FSMContext) -> None:
    try:
        to_val = parse_float(message.text or "")
    except ValidationError as exc:
        await _handle_validation_error(message, exc)
        return
    data = await state.get_data()
    from_val: float = data["from_val"]
    result = percent_change(from_val, to_val)
    sign = "+" if result.value >= 0 else ""
    text = RESULT_CHANGE.format(
        from_val=fmt_input(from_val),
        to_val=fmt_input(to_val),
        result=f"{sign}{fmt_number(result.value)}",
    )
    await _send_result(message, state, text)


# ════════════════════════════════════════════════════════════════════════════
# MODE 4 — Кредитный калькулятор
# ════════════════════════════════════════════════════════════════════════════

@router.callback_query(lambda c: c.data == CB_LOAN)
async def start_loan(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    await state.set_state(LoanStates.waiting_amount)
    await callback.message.answer(ASK_LOAN_AMOUNT, parse_mode="HTML")  # type: ignore[union-attr]


@router.message(LoanStates.waiting_amount)
async def got_loan_amount(message: Message, state: FSMContext) -> None:
    try:
        amount = parse_positive_float(message.text or "")
    except ValidationError as exc:
        await _handle_validation_error(message, exc)
        return
    await state.update_data(amount=amount)
    await state.set_state(LoanStates.waiting_rate)
    await _ask(message, ASK_LOAN_RATE)


@router.message(LoanStates.waiting_rate)
async def got_loan_rate(message: Message, state: FSMContext) -> None:
    try:
        rate = parse_positive_float(message.text or "")
    except ValidationError as exc:
        await _handle_validation_error(message, exc)
        return
    await state.update_data(rate=rate)
    await state.set_state(LoanStates.waiting_months)
    await _ask(message, ASK_LOAN_MONTHS)


@router.message(LoanStates.waiting_months)
async def got_loan_months(message: Message, state: FSMContext) -> None:
    try:
        months = parse_steps(message.text or "")
    except ValidationError as exc:
        await _handle_validation_error(message, exc)
        return
    data = await state.get_data()
    amount: float = data["amount"]
    rate: float = data["rate"]
    result = loan_annuity(amount, rate, months)
    text = RESULT_LOAN.format(
        amount=fmt_number(amount),
        rate=fmt_input(rate),
        months=months,
        monthly=fmt_number(result.monthly_payment),
        total=fmt_number(result.total_payment),
        overpay=fmt_number(result.overpayment),
    )
    await _send_result(message, state, text)


# ════════════════════════════════════════════════════════════════════════════
# MODE 5 — Вклад в банке
# ════════════════════════════════════════════════════════════════════════════

@router.callback_query(lambda c: c.data == CB_DEPOSIT)
async def start_deposit(callback: CallbackQuery, state: FSMContext) -> None:
    """Show deposit type selection."""
    await callback.answer()
    await callback.message.answer(  # type: ignore[union-attr]
        "Выбери тип вклада:",
        reply_markup=deposit_menu_keyboard(),
        parse_mode="HTML",
    )


# ── Без капитализации ─────────────────────────────────────────────────────────

@router.callback_query(lambda c: c.data == CB_DEPOSIT_SIMPLE)
async def start_deposit_simple(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    await state.set_state(DepositStates.waiting_amount)
    await callback.message.answer(ASK_DEPOSIT_AMOUNT, parse_mode="HTML")  # type: ignore[union-attr]


@router.message(DepositStates.waiting_amount)
async def got_deposit_simple_amount(message: Message, state: FSMContext) -> None:
    try:
        amount = parse_positive_float(message.text or "")
    except ValidationError as exc:
        await _handle_validation_error(message, exc)
        return
    await state.update_data(amount=amount)
    await state.set_state(DepositStates.waiting_rate)
    await _ask(message, ASK_DEPOSIT_RATE)


@router.message(DepositStates.waiting_rate)
async def got_deposit_simple_rate(message: Message, state: FSMContext) -> None:
    try:
        rate = parse_positive_float(message.text or "")
    except ValidationError as exc:
        await _handle_validation_error(message, exc)
        return
    await state.update_data(rate=rate)
    await state.set_state(DepositStates.waiting_months)
    await _ask(message, ASK_DEPOSIT_MONTHS)


@router.message(DepositStates.waiting_months)
async def got_deposit_simple_months(message: Message, state: FSMContext) -> None:
    try:
        months = parse_steps(message.text or "")
    except ValidationError as exc:
        await _handle_validation_error(message, exc)
        return
    data = await state.get_data()
    amount: float = data["amount"]
    rate: float = data["rate"]
    result = deposit_simple(amount, rate, months)
    text = RESULT_DEPOSIT.format(
        amount=fmt_number(amount),
        rate=fmt_input(rate),
        months=months,
        total=fmt_number(result.total),
        profit=fmt_number(result.profit),
    )
    await _send_result(message, state, text)


# ── С капитализацией ──────────────────────────────────────────────────────────

@router.callback_query(lambda c: c.data == CB_DEPOSIT_COMPOUND)
async def start_deposit_compound(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    await state.set_state(DepositCompoundStates.waiting_amount)
    await callback.message.answer(ASK_DEPOSIT_AMOUNT, parse_mode="HTML")  # type: ignore[union-attr]


@router.message(DepositCompoundStates.waiting_amount)
async def got_deposit_compound_amount(message: Message, state: FSMContext) -> None:
    try:
        amount = parse_positive_float(message.text or "")
    except ValidationError as exc:
        await _handle_validation_error(message, exc)
        return
    await state.update_data(amount=amount)
    await state.set_state(DepositCompoundStates.waiting_rate)
    await _ask(message, ASK_DEPOSIT_RATE)


@router.message(DepositCompoundStates.waiting_rate)
async def got_deposit_compound_rate(message: Message, state: FSMContext) -> None:
    try:
        rate = parse_positive_float(message.text or "")
    except ValidationError as exc:
        await _handle_validation_error(message, exc)
        return
    await state.update_data(rate=rate)
    await state.set_state(DepositCompoundStates.waiting_months)
    await _ask(message, ASK_DEPOSIT_MONTHS)


@router.message(DepositCompoundStates.waiting_months)
async def got_deposit_compound_months(message: Message, state: FSMContext) -> None:
    try:
        months = parse_steps(message.text or "")
    except ValidationError as exc:
        await _handle_validation_error(message, exc)
        return
    data = await state.get_data()
    amount: float = data["amount"]
    rate: float = data["rate"]
    result = deposit_compound(amount, rate, months)
    text = RESULT_DEPOSIT_COMPOUND.format(
        amount=fmt_number(amount),
        rate=fmt_input(rate),
        months=months,
        total=fmt_number(result.total),
        profit=fmt_number(result.profit),
    )
    await _send_result(message, state, text)
