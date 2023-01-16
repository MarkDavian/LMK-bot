import multiprocessing
import asyncio
import logging


from bot.core.data_master.master import start_data_master
from bot.connectors.register import start_connectors


async def main():
    await start_connectors()

def run_main():
    asyncio.run(main())


if __name__ == "__main__":
    main_proc = multiprocessing.Process(target=run_main)
    dup = multiprocessing.Process(target=start_data_master)

    main_proc.start()
    dup.start()


# main_logger = logging.getLogger(__name__)
# main_logger.setLevel(logging.INFO)
# handler = logging.FileHandler(f"Main.log", mode='w')
# formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")
# handler.setFormatter(formatter)
# main_logger.addHandler(handler)

# main_logger.info('Main started')
