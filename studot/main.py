import multiprocessing
import asyncio
import logging

from prometheus_client import start_http_server

logging.basicConfig(
    level=logging.INFO, 
    filename='logs/all.log'
)

from bot.core.data_master.master import start_data_master
from bot.connectors.register import start_connectors

from bot.core.notifier.notifier import start_notifier


main_logger = logging.getLogger(__name__)
main_logger.setLevel(logging.INFO)
handler = logging.FileHandler(f"logs/Main.log", mode='w')
formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")
handler.setFormatter(formatter)
main_logger.addHandler(handler)
main_logger.addHandler(logging.StreamHandler())


async def main():
    main_logger.info('Main started')
    start_http_server(9877)
    await start_connectors()


def run_main():
    asyncio.run(main())


if __name__ == "__main__":
    main_proc = multiprocessing.Process(target=run_main)
    master_proc = multiprocessing.Process(target=start_data_master)
    notifier_proc = multiprocessing.Process(target=start_notifier)

    main_proc.start()
    master_proc.start()
    notifier_proc.start()
