#!/bin/bash

function execute_cql {
  until echo "$1" | cqlsh; do
    echo "cqlsh: Cassandra is unavailable - retrying later"
    sleep 2
  done
}

if [[ ! -z "$CASSANDRA_KEYSPACE" && $1 = 'cassandra' ]]; then
  # Create default keyspace for single node cluster
  CQL="CREATE KEYSPACE IF NOT EXISTS productViews
        WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};

        USE productViews;

        CREATE TABLE IF NOT EXISTS product_views (
          messageid TEXT,
          event TEXT,
          userid TEXT,
          productid TEXT,
          source TEXT,
          messagetime TIMESTAMP,
          PRIMARY KEY (userid, productid, messageid, messagetime)
        );
		
		CREATE TABLE IF NOT EXISTS order_views (
		  orderid TEXT,
		  productid TEXT,
		  categoryid TEXT,
		  quantity INT,
		  userid TEXT,
		  messagetime TIMESTAMP,
		  PRIMARY KEY (userid, productid, messagetime)
		);"

  execute_cql "$CQL" &

  # Add ALLOW_FILTERING option
  cqlsh -e "UPDATE system.settings SET allow_filtering = true;" &
fi

exec /docker-entrypoint.sh "$@"