import asyncio
from datetime import datetime

async def alive(bot):
    while True:
        if bot.is_closed():
            print(datetime.utcnow())
        await asyncio.sleep(5)