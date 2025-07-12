import aiosqlite
import asyncio

async def async_fetch_users():
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT * FROM users") as cursor:
            row = await cursor.fetchall()
            return row

        
async def async_fetch_older_users():
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT * FROM users WHERE age > ?", (40,)) as cursor:
            rows = await cursor.fetchall()
            return rows


async def fetch_concurrently():
    results = await asyncio.gather(
        async_fetch_older_users(),
        async_fetch_users(),
    )
    older_users, all_users = results
    print("Users older than 40:", older_users)
    print("All users:", all_users)
    
asyncio.run(fetch_concurrently())
    