import asyncio

import asyncpg


class Table_Create:
    def __init__(self, user, password, database, host, port=5432):
        self.user = user
        self.password = password
        self.database = database
        self.host = host
        self.port = port

    async def connect(self):
        self.connect = await asyncpg.connect(
            user=self.user,
            password=self.password,
            database=self.database,
            host=self.host,
            port=self.port
        )

    async def table_users(self):
        await self.connect.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id SERIAL PRIMARY KEY,
            tg_id BIGINT UNIQUE,
            warn int DEFAULT 0
        );

        """)

    async def drop_table(self, table: str):
        await self.connect.execute(f"""
            DROP TABLE ({table})
        """)

    async def close(self):
        await self.connect.close()


async def main():
    db = Table_Create(
        user='postgres',
        password='Timur',
        database='moderrework',
        host='localhost',
        port=5432
    )

    try:
        await db.connect()
        await db.table_users()
    except (OSError, asyncpg.PostgresError) as e:
        print(f"Ебанат блять, запросы настрой нормально: {e}")
    finally:
        await db.close()
