import datetime

import aiofiles
from aiopath import AsyncPath


async def log_exchange_command(command, response):
    log_dir = AsyncPath('logs')
    await log_dir.mkdir(exist_ok=True)
    log_file = log_dir / f"{datetime.datetime.now().strftime('%Y-%m-%d')}.log"

    async with aiofiles.open(log_file, mode='a') as f:
        log_entry = f"{datetime.datetime.now().isoformat()} - Command: {command}, Response: {response}\n"
        await f.write(log_entry)
