import random
import uuid
import os

import psycopg2
from dotenv import load_dotenv

### This script enables the necessary tests to be performed by loading test data into the PostgreSQL database

load_dotenv()

conn = psycopg2.connect(
    dbname=os.getenv("POSTGRES_DB_NAME"),
    user=os.getenv("POSTGRES_DB_USER"),
    password=os.getenv("POSTGRES_DB_PASSWORD"),
    host=os.getenv("POSTGRES_DB_HOST")
)

cur = conn.cursor()

def main():
    # Generate product_id list for create table
    product_id_list = list()
    for num in range(1000):
        product_id_list.append("product-" + str(num))

    random.shuffle(product_id_list)

    # Generate user_id list
    user_id_list = list()
    for num in range(100):
        user_id_list.append("user-" + str(num))

    for product_id in product_id_list:

        # randomly determine which category this product belongs to
        category_id = "category-" + str(random.randint(1, 4))

        # Create product 
        cur.execute("""
            INSERT INTO products (product_id, category_id) 
            VALUES (%s, %s)
        """, (product_id, category_id))

        for _ in range(random.randint(1, 200)): # Generate the number of random purchases of a product

            # Generate unique uuid for order_id
            order_id = str(uuid.uuid4()) 

            # Pick random user_id
            user_id = random.choice(user_id_list) 

            # BETWEEN (June 1, 2023) AND (June 1, 2024) 
            timestamp = random.randint(1685581261, 1717203661) 

            # Create order
            cur.execute("""
                INSERT INTO orders (order_id, user_id, timestamp) 
                VALUES (%s, %s, %s)
            """, (order_id, user_id, timestamp))

            # Generate random order quantity value
            order_item_quantity = random.randint(1, 5) 

            # Create order item
            cur.execute("""
                INSERT INTO order_items (order_id, product_id, quantity) 
                VALUES (%s, %s, %s)
            """, (order_id, product_id, order_item_quantity))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()
