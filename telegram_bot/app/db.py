import os
import asyncpg

pool: asyncpg.pool.Pool | None = None

async def create_pool(dsn: str):
    global pool
    pool = await asyncpg.create_pool(dsn)
    return pool

async def close_pool():
    global pool
    if pool:
        await pool.close()

async def init_db():
    """Create tables if they do not exist."""
    global pool
    if not pool:
        raise RuntimeError("Pool is not initialized")
    async with pool.acquire() as conn:
        await conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            telegram_id BIGINT UNIQUE,
            username TEXT,
            first_name TEXT,
            last_name TEXT,
            phone TEXT,
            email TEXT,
            address TEXT
        );
        ''')
        await conn.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
            product TEXT,
            quantity INTEGER,
            delivery_address TEXT,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
        );
        ''')

async def save_user_and_order(telegram_user: dict, order: dict):
    """Insert or update user and insert order. Returns order id."""
    global pool
    if not pool:
        raise RuntimeError("Pool is not initialized")

    async with pool.acquire() as conn:
        # Upsert user by telegram_id
        user_row = await conn.fetchrow('''
            INSERT INTO users (telegram_id, username, first_name, last_name, phone, email, address)
            VALUES ($1,$2,$3,$4,$5,$6,$7)
            ON CONFLICT (telegram_id) DO UPDATE SET
              username = EXCLUDED.username,
              first_name = EXCLUDED.first_name,
              last_name = EXCLUDED.last_name,
              phone = EXCLUDED.phone,
              email = EXCLUDED.email,
              address = EXCLUDED.address
            RETURNING id;
        ''',
        telegram_user.get('telegram_id'),
        telegram_user.get('username'),
        telegram_user.get('first_name'),
        telegram_user.get('last_name'),
        telegram_user.get('phone'),
        telegram_user.get('email'),
        telegram_user.get('address'))

        user_id = user_row['id']

        order_row = await conn.fetchrow('''
            INSERT INTO orders (user_id, product, quantity, delivery_address)
            VALUES ($1,$2,$3,$4) RETURNING id;
        ''', user_id, order.get('product'), int(order.get('quantity') or 1), order.get('delivery_address'))

        return order_row['id']
