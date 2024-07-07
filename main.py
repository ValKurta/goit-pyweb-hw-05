import argparse
import asyncio
import json
from datetime import datetime, timedelta

from ccy_exchange import CurrencyExchange


async def main():
    parser = argparse.ArgumentParser(description='Get currency exchange rates from PB.')
    parser.add_argument('days', type=int, help='Number of days to retrieve exchange rates for')
    parser.add_argument('--currencies', type=str, nargs='+', default=['EUR', 'USD'],
                        help='List of currencies to retrieve exchange rates for')

    args = parser.parse_args()

    if not 2 <= args.days <= 10:
        print("Please provide a number of days between 2 and 10.")
        return

    end_date = datetime.now()
    start_date = end_date - timedelta(days=args.days)

    currency_exchange = CurrencyExchange()
    rates = await currency_exchange.get_exchange_rates(start_date, end_date, args.currencies)

    result = []
    for date, rate in rates.items():
        result.append({date: rate})

    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    asyncio.run(main())
