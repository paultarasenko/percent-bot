"""
Formatting helpers.
Keeps presentation logic away from business logic and handlers.
"""
from config import settings


def fmt_number(value: float) -> str:
    """
    Format a float for display with adaptive precision.
    - Very small numbers (abs < 1e-6): scientific notation
    - Normal numbers: strip trailing zeros, up to result_precision decimals
    """
    if value != 0 and abs(value) < 1e-6:
        return f"{value:.2e}"
    formatted = f"{value:.{settings.result_precision}f}".rstrip("0").rstrip(".")
    return formatted


def fmt_input(value: float) -> str:
    """
    Format a user-provided input value for display in result messages.
    Same logic as fmt_number — keeps results readable.
    """
    return fmt_number(value)
