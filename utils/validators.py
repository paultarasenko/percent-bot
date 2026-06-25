"""
Input validation helpers used across all handlers.
Each function either returns a parsed value or raises ValueError with a user-friendly key.
"""
from config import settings


class ValidationError(Exception):
    """Carries the text key to be shown to the user."""
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


def parse_float(text: str) -> float:
    """
    Parse user input as float.

    Raises:
        ValidationError: if the text is not a valid number or exceeds max input value.
    """
    try:
        value = float(text.replace(",", ".").strip())
    except ValueError:
        from texts.messages import ERR_NOT_A_NUMBER
        raise ValidationError(ERR_NOT_A_NUMBER)

    if abs(value) > settings.max_input_value:
        from texts.messages import ERR_VALUE_TOO_LARGE
        raise ValidationError(ERR_VALUE_TOO_LARGE)

    return value


def parse_positive_float(text: str) -> float:
    """
    Parse a strictly positive float.

    Raises:
        ValidationError: if value ≤ 0.
    """
    value = parse_float(text)
    if value <= 0:
        from texts.messages import ERR_NEGATIVE_NOT_ALLOWED
        raise ValidationError(ERR_NEGATIVE_NOT_ALLOWED)
    return value


def parse_nonzero_float(text: str) -> float:
    """
    Parse any float that is not zero (allows negatives).

    Raises:
        ValidationError: if value == 0.
    """
    value = parse_float(text)
    if value == 0:
        from texts.messages import ERR_ZERO_FROM
        raise ValidationError(ERR_ZERO_FROM)
    return value


def parse_steps(text: str) -> int:
    """
    Parse a positive integer number of steps.

    Raises:
        ValidationError: if not an integer or exceeds max_steps.
    """
    stripped = text.strip()
    if not stripped.lstrip("-").isdigit():
        from texts.messages import ERR_STEPS_NOT_INT
        raise ValidationError(ERR_STEPS_NOT_INT)

    value = int(stripped)
    if value <= 0:
        from texts.messages import ERR_NEGATIVE_NOT_ALLOWED
        raise ValidationError(ERR_NEGATIVE_NOT_ALLOWED)

    if value > settings.max_steps:
        from texts.messages import ERR_STEPS_TOO_LARGE
        raise ValidationError(ERR_STEPS_TOO_LARGE.format(max_steps=settings.max_steps))

    return value
