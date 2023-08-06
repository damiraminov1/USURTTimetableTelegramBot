import asyncio

from app.bot.bot import bot, dp


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
