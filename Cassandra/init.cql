CREATE KEYSPACE IF NOT EXISTS productViews WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'};

USE productViews;

CREATE TABLE IF NOT EXISTS product_views (
    messageid UUID,
    event TEXT,
    userid UUID,
    productid UUID,
    source TEXT,
    timestamp TIMESTAMP,
    PRIMARY KEY (messageid)
);
