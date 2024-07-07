import asyncio
from datetime import timedelta

import aiohttp


class PrivatBankAPI:
    BASE_URL = 'https://api.privatbank.ua/p24api/exchange_rates?json&date='

    @staticmethod
    async def fetch_exchange_rate(session, date):
        url = f"{PrivatBankAPI.BASE_URL}{date}"
        try:
            async with session.get(url) as response:
                response.raise_for_status()
                return await response.json()
        except aiohttp.ClientError as e:
            print(f"Failed to fetch data for {date}: {e}")
            return None

    async def get_exchange_rates(self, start_date, end_date, currencies):
        rates = {}
        async with aiohttp.ClientSession() as session:
            tasks = []
            current_date = start_date
            while current_date <= end_date:
                formatted_date = current_date.strftime('%d.%m.%Y')
                tasks.append(self.fetch_exchange_rate(session, formatted_date))
                current_date += timedelta(days=1)

            results = await asyncio.gather(*tasks)

        for result in results:
            if result:
                date = result['date']
                daily_rates = {}
                for exchange_rate in result['exchangeRate']:
                    currency = exchange_rate['currency']
                    if currency in currencies:
                        daily_rates[currency] = {
                            'sale': exchange_rate.get('saleRate', None),
                            'purchase': exchange_rate.get('purchaseRate', None)
                        }
                if daily_rates:
                    rates[date] = daily_rates
        return rates
