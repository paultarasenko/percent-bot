"""
Application configuration loaded from environment variables / .env file.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Bot configuration. All values can be overridden via environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # ── Required ──────────────────────────────────────────────────────────────
    bot_token: str

    # ── Logging ───────────────────────────────────────────────────────────────
    log_level: str = "INFO"

    # ── Webhook (optional, polling is the default) ────────────────────────────
    use_webhook: bool = False
    webhook_host: str = ""
    webhook_path: str = "/webhook"
    webhook_port: int = 8080

    # ── Calculator limits ─────────────────────────────────────────────────────
    max_steps: int = 100_000       # upper bound for compound steps
    max_input_value: float = 1e15  # upper bound for any numeric input
    result_precision: int = 6      # decimal places in results


settings = Settings()  # type: ignore[call-arg]
