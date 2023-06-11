import asyncio
import time
import aiohttp
import logging
from datetime import datetime, timedelta
import platform
import sys 


pb_url = 'https://api.privatbank.ua/p24api/exchange_rates?json&date='


class PBCollector:
    def __init__(self):
        self.session = aiohttp.ClientSession()

    async def get_currency(self, days: int):
        async with self.session as session:
            tasks = []
            today = datetime.today()
            for i in range(days):
                day = (today - timedelta(days=i)).strftime('%d.%m.%Y')
                tasks.append(self.get_currency_rate(session, day))
            results = await asyncio.gather(*tasks)
            return results

    @staticmethod
    async def get_currency_rate(session: aiohttp.ClientSession, day: str):
        logging.debug('Started!')
        start = time.time()
        async with session.get(pb_url+day) as response:
            result = await response.json()
            finish = time.time()
            logging.info(f'done in {finish - start:.4f} sec.')
            return result


async def main():
    nums_day = int(sys.argv[1])
    pb = PBCollector()
    result = await pb.get_currency(nums_day)
    logging.info(f"Getting currency rate for past {nums_day} days.")

    logging.debug("Results:")
    for i in result:
        logging.debug(i)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG,
                        format='[%(levelname)s] %(funcName)s %(message)s')
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
