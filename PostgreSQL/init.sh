#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
	CREATE DATABASE product_views;
	GRANT ALL PRIVILEGES ON DATABASE product_views TO postgres;
	CREATE DATABASE product_match_django;
	GRANT ALL PRIVILEGES ON DATABASE product_match_django TO postgres;
	CREATE DATABASE airflow;
	GRANT ALL PRIVILEGES ON DATABASE airflow TO postgres;
EOSQL

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "product_views" <<-EOSQL
	CREATE TABLE products (
		product_id VARCHAR(255) PRIMARY KEY,
		category_id VARCHAR(255)
	);

	CREATE TABLE orders (
		order_id VARCHAR(255) PRIMARY KEY,
		user_id VARCHAR(255),
		timestamp INT
	);

	CREATE TABLE order_items (
		id SERIAL PRIMARY KEY,
		order_id VARCHAR(255) REFERENCES orders(order_id),
		product_id VARCHAR(255) REFERENCES products(product_id),
		quantity INT
	);
EOSQL