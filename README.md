## Real-Time Recommendation Engine for E-commerce Platform


## Summary


This is a real-time recommendation engine that can operate within an e-commerce platform. It encompasses ETL processes, a Q mechanism, and Time Series databases. It operates with a Docker-compose file. To initiate, type the following command:

```bash
docker-compose up -d --build
```



## Architecture

![Architecture](/Documantation/Drawings/product_match.png)


This platform reads products from a JSON file, sends them to Kafka first, and then stores them in a time series database. ETL processes manage the data flow between PostgreSQL and Cassandra. Django exposes recommended data through API services. All services run within Docker containers.


All services include their own init scripts. There is **no need to create tables or configure anything** in any database. These processes occur during the initial build of the containers.

### Cassandra

Cassandra contains 2 tables. One of the tables contains visited products, while the other contains orders. Their names are *product_views* and *order_views*.

productviews Keyspace


product_views          =>     messageid TEXT    |   event TEXT      |   userid TEXT      |   productid TEXT   |   source TEXT  |   messagetime TIMESTAMP


order_views            =>     orderid TEXT      |   productid TEXT  |   categoryid TEXT  |   quantity INT     |   userid TEXT  |   messagetime TIMESTAMP

### Airflow

### Kafka


