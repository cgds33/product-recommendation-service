FROM cassandra:3.0.20
	
ENV CASSANDRA_KEYSPACE productViews
ENV TABLE product_views

COPY entrypoint-wrap.sh /entrypoint-wrap.sh
ENTRYPOINT ["/entrypoint-wrap.sh"]
CMD ["cassandra", "-f"]