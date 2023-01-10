import asyncio
from bot.connectors.register import start_connectors


async def main():
    await start_connectors()


if __name__ == "__main__":
    asyncio.run(main())