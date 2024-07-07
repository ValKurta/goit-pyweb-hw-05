import asyncio
import websockets
import json


async def test_exchange_command(days, currencies):
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        command = {
            "command": "exchange",
            "days": days,
            "currencies": currencies
        }
        await websocket.send(json.dumps(command))

        response = await websocket.recv()
        print(f"Received response: {response}")

if __name__ == '__main__':
    days = 7
    currencies = ["EUR", "USD"]
    asyncio.run(test_exchange_command(days, currencies))
