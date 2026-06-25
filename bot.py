"""
Bot entry point.

Runs in polling mode by default.
To switch to webhook: set USE_WEBHOOK=true in .env and configure
WEBHOOK_HOST, WEBHOOK_PATH, WEBHOOK_PORT.
The rest of the codebase is not affected by this choice.
"""
import asyncio
import logging
import sys
from pathlib import Path

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

from config import settings
from handlers import get_all_routers


def setup_logging() -> None:
    """Configure root logger. Log to stdout and to logs/bot.log."""
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    handlers: list[logging.Handler] = [
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(log_dir / "bot.log", encoding="utf-8"),
    ]

    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper(), logging.INFO),
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=handlers,
    )


def create_bot() -> Bot:
    """Instantiate Bot with HTML parse mode as default."""
    return Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )


def create_dispatcher() -> Dispatcher:
    """Create Dispatcher with in-memory FSM storage and register all routers."""
    dp = Dispatcher(storage=MemoryStorage())
    for router in get_all_routers():
        dp.include_router(router)
    return dp


# ── Polling ───────────────────────────────────────────────────────────────────

async def run_polling(bot: Bot, dp: Dispatcher) -> None:
    """Start long-polling. Drops pending updates on start."""
    logger = logging.getLogger(__name__)
    logger.info("Starting in polling mode")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


# ── Webhook ───────────────────────────────────────────────────────────────────

async def run_webhook(bot: Bot, dp: Dispatcher) -> None:
    """Start aiohttp server and register webhook with Telegram."""
    logger = logging.getLogger(__name__)
    webhook_url = f"{settings.webhook_host}{settings.webhook_path}"
    logger.info("Starting in webhook mode: %s", webhook_url)

    await bot.set_webhook(webhook_url, drop_pending_updates=True)

    app = web.Application()
    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=settings.webhook_path)
    setup_application(app, dp, bot=bot)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host="0.0.0.0", port=settings.webhook_port)
    await site.start()

    logger.info("Webhook server listening on port %s", settings.webhook_port)

    # Keep running until interrupted
    await asyncio.Event().wait()


# ── Main ──────────────────────────────────────────────────────────────────────

async def main() -> None:
    setup_logging()
    logger = logging.getLogger(__name__)

    bot = create_bot()
    dp = create_dispatcher()

    try:
        if settings.use_webhook:
            await run_webhook(bot, dp)
        else:
            await run_polling(bot, dp)
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped")
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
