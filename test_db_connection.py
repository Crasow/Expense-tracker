import asyncio
import asyncpg

async def test_connection():
    try:
        # Попробуем подключиться к базе данных postgres (которая должна существовать по умолчанию)
        conn = await asyncpg.connect(
            host='localhost',
            port=5433,
            user='postgres',
            password='9129',  # Пароль из конфигурации
            database='postgres'
        )
        print("✅ Подключение к PostgreSQL успешно!")
        
        # Проверим, существует ли база данных expense_db
        result = await conn.fetchval(
            "SELECT 1 FROM pg_database WHERE datname = $1", 
            'expense_db'
        )
        
        if result:
            print("✅ База данных 'expense_db' существует")
        else:
            print("❌ База данных 'expense_db' не существует")
            print("Создаем базу данных...")
            await conn.execute("CREATE DATABASE expense_db")
            print("✅ База данных 'expense_db' создана")
        
        await conn.close()
        
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")

if __name__ == "__main__":
    asyncio.run(test_connection()) 