"""
Formatting helpers.
Keeps presentation logic away from business logic and handlers.
"""
from config import settings


def fmt_number(value: float) -> str:
    """
    Format a float for display.
    - Strips unnecessary trailing zeros.
    - Uses up to `settings.result_precision` decimal places.

    Examples:
        100.0     → "100"
        5.0       → "5"
        3778.343  → "3778.343"
        0.025     → "0.025"
    """
    formatted = f"{value:.{settings.result_precision}f}".rstrip("0").rstrip(".")
    return formatted


def fmt_input(value: float) -> str:
    """
    Format a user-provided input value for display in result messages.
    Same logic as fmt_number — keeps results readable.
    """
    return fmt_number(value)
