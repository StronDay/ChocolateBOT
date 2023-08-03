import asyncio
from data_base import sql_worker

async def schedule_task():
    while True:
        await sql_worker.check_remaining_time()
        await asyncio.sleep(60)