import json
import asyncio
import aiofiles
import websockets

from aiopath import AsyncPath
from datetime import datetime, timedelta
from ccy_exchange import CurrencyExchange


class WebSocketServer:
    def __init__(self):
        self.clients = set()

    async def register(self, websocket):
        self.clients.add(websocket)

    async def unregister(self, websocket):
        self.clients.remove(websocket)

    async def send_to_clients(self, message):
        if self.clients:
            await asyncio.wait([client.send(message) for client in self.clients])

    async def handler(self, websocket, path):
        await self.register(websocket)
        try:
            async for message in websocket:
                data = json.loads(message)
                if data.get('command') == 'exchange':
                    days = int(data.get('days', 1))
                    currencies = data.get('currencies', ['EUR', 'USD'])
                    await self.handle_exchange_command(websocket, days, currencies)
        finally:
            await self.unregister(websocket)

    async def handle_exchange_command(self, websocket, days, currencies):
        if not 1 <= days <= 10:
            await websocket.send(json.dumps({"error": "Number of days must be between 1 and 10"}))
            return

        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        currency_exchange = CurrencyExchange()
        rates = await currency_exchange.get_exchange_rates(start_date, end_date, currencies)

        response = json.dumps(rates, ensure_ascii=False, indent=2)
        await websocket.send(response)

        await self.log_exchange_command(days, currencies, response)

    async def log_exchange_command(self, days, currencies, response):
        log_dir = AsyncPath('logs')
        await log_dir.mkdir(exist_ok=True)
        log_file = log_dir / f"{datetime.now().strftime('%Y-%m-%d')}.log"

        async with aiofiles.open(log_file, mode='a') as f:
            log_entry = (f"{datetime.now().isoformat()} - Command: exchange, Days: {days}, Currencies: {currencies},"
                         f" Response: {response}\n")
            await f.write(log_entry)


async def main():
    server = WebSocketServer()
    start_server = websockets.serve(server.handler, "localhost", 8765)
    await start_server
    await asyncio.Future()


if __name__ == '__main__':
    asyncio.run(main())
