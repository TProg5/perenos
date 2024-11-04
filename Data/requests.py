import asyncpg
import asyncio


async def add_user(tg_id: int):
    connect = await asyncpg.connect(
        user='postgres',
        password='Timur',
        database='moderrework',
        host='localhost',
        port=5432
    )
    # версия добавления юзера, только в postgresql
    # await connect.execute(f"""
    #     DO $$
    #     BEGIN
    #         IF NOT EXISTS (SELECT 1 FROM users WHERE tg_id = {tg_id}) THEN
    #             INSERT INTO users (tg_id) VALUES ({tg_id});
    #         END IF;
    #     END $$;
    # """)

    # одно из расширений postgresql 
    # await connect.execute(f"""
    #     INSERT INTO users (tg_id) VALUES ({tg_id})
    #     ON CONFLICT DO NOTHING;
    # """)

    # True SQL
    await connect.execute(f"""
        INSERT INTO users (tg_id)
        SELECT {tg_id}
        WHERE NOT EXISTS (
        SELECT 1 FROM users WHERE tg_id = {tg_id});
    """)
    await connect.close()


async def check_warns(tg_id: int):
    connect = await asyncpg.connect(
        user='postgres',
        password='Timur',
        database='moderrework',
        host='localhost',
        port=5432
    )

    warn = await connect.fetchval(f"""
        SELECT warn FROM users WHERE tg_id = {tg_id};
    """)

    return warn


async def add_warn(znak: str, count: int, tg_id: int):
    connect = await asyncpg.connect(
        user='postgres',
        password='Timur',
        database='moderrework',
        host='localhost',
        port=5432
    )

    await connect.execute(f"""
        UPDATE users SET warn = warn {znak} {count} WHERE tg_id = $1;
    """, tg_id)


