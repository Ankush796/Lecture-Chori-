#  MIT License

import os
import asyncio
import logging
from logging.handlers import RotatingFileHandler

from config import Config
from pyrogram import Client, idle
from pyromod import listen

LOGGER = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(name)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        RotatingFileHandler("log.txt", maxBytes=5000000, backupCount=10),
        logging.StreamHandler(),
    ],
)

# Auth Users
AUTH_USERS = [int(x) for x in Config.AUTH_USERS.split(",") if x]

plugins = dict(root="plugins")


# ─── Tiny HTTP Server For Render ─────────────────────────────
async def start_health_server():
    port = int(os.getenv("PORT", "0"))
    if port == 0:
        return

    try:
        from aiohttp import web
        async def ok(_):
            return web.Response(text="ok")

        app = web.Application()
        app.router.add_get("/", ok)
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, "0.0.0.0", port)
        await site.start()
        LOGGER.info(f"Health server running on port {port}")

    except Exception as e:
        LOGGER.warning(f"Health server error: {e}")


# ─── BOT ─────────────────────────────────────────────────────
bot = Client(
    "StarkBot",
    bot_token=Config.BOT_TOKEN,
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    sleep_threshold=20,
    plugins=plugins,
    workers=50
)


async def main():
    await start_health_server()
    await bot.start()
    me = await bot.get_me()
    LOGGER.info(f"<--- @{me.username} Started (c) STARKBOT --->")
    await idle()


if __name__ == "__main__":
    asyncio.run(main())
    LOGGER.info("<--- Bot Stopped --->")
