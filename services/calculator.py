"""
Pure calculation functions.
No Telegram, no I/O — just math.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class CalcResult:
    """Unified container for a calculator result."""
    value: float
    is_percentage: bool = False


@dataclass(frozen=True)
class LoanResult:
    """Result of a loan calculation."""
    monthly_payment: float
    total_payment: float
    overpayment: float


@dataclass(frozen=True)
class DepositResult:
    """Result of a simple interest deposit calculation."""
    total: float
    profit: float


def percent_of(percent: float, number: float) -> CalcResult:
    """X% of a number. Example: 50% of 200 → 100.0"""
    return CalcResult(value=(percent / 100) * number)


def what_percent(part: float, whole: float) -> CalcResult:
    """What % is part of whole. Example: 10 of 200 → 5.0%"""
    return CalcResult(value=(part / whole) * 100, is_percentage=True)


def percent_change(from_val: float, to_val: float) -> CalcResult:
    """% change from one value to another. Example: 20 → 100 = +400%"""
    return CalcResult(value=((to_val - from_val) / from_val) * 100, is_percentage=True)


def loan_annuity(amount: float, annual_rate_percent: float, months: int) -> LoanResult:
    """
    Annuity loan payment.
    Formula: M = P × r × (1+r)^n / ((1+r)^n - 1)
    """
    monthly_rate = annual_rate_percent / 100 / 12
    if monthly_rate == 0:
        monthly = amount / months
    else:
        monthly = amount * monthly_rate * (1 + monthly_rate) ** months / ((1 + monthly_rate) ** months - 1)
    total = monthly * months
    return LoanResult(monthly_payment=monthly, total_payment=total, overpayment=total - amount)


def deposit_simple(amount: float, annual_rate_percent: float, months: int) -> DepositResult:
    """
    Simple interest deposit.
    Formula: profit = amount × rate/100 × months/12
    """
    profit = amount * (annual_rate_percent / 100) * (months / 12)
    return DepositResult(total=amount + profit, profit=profit)


def deposit_compound(amount: float, annual_rate_percent: float, months: int) -> DepositResult:
    """
    Compound interest deposit with monthly capitalization.
    Formula: total = amount × (1 + rate/12/100) ^ months
    """
    monthly_rate = annual_rate_percent / 100 / 12
    total = amount * (1 + monthly_rate) ** months
    return DepositResult(total=total, profit=total - amount)
