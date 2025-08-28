import logging
import json
import psycopg2

from dotenv import dotenv_values

try:
    env_vars = dotenv_values(".env")
    DB_CONFIG = {
        "dbname": env_vars['DB_NAME'],
        "user": env_vars['DB_USER'],
        "password": env_vars['DB_PASSWORD'],
        "host": "localhost",  # or your db host
        "port": "5432"       # default postgres port
    }
except Exception as e:
    print(e)
    print('Создайте файл .env.')


with open("ozon_orders.json", "r") as file:
    data = json.load(file)


def main(config, data ):
    """Функция принимает в себя json файл и настройки подключения в БД. """

    try:
        print("Подключение к БД...")
        conn = psycopg2.connect(**config)
        cursor = conn.cursor()


        print("Выгрузка данных в БД...")
        for record in data:
            customer_data = record['customer']

            insert_customer_sql = """
            INSERT INTO customerregions (id, region) VALUES (%s, %s)
            ON CONFLICT (id) DO NOTHING;
            """
            cursor.execute(insert_customer_sql, (customer_data['id'], customer_data['region']))

            insert_order_sql = """
            INSERT INTO orders (order_id, status, date, amount, customer_region_id)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (order_id) DO UPDATE SET
                status = EXCLUDED.status,
                date = EXCLUDED.date,
                amount = EXCLUDED.amount,
                customer_region_id = EXCLUDED.customer_region_id;
            """
            cursor.execute(insert_order_sql, (
                record['order_id'], 
                record['status'], 
                record['date'], 
                record['amount'], 
                customer_data['id']
            ))

        conn.commit()
        print("Данные были успешно выгружены в PostgreSQL.")

    except Exception as e:
        print(f"Ошибка: {e}")
        
if __name__ == "__main__":
    main(DB_CONFIG, data)

