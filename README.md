## Real-Time Recommendation Engine for E-commerce Platform


## Summary


This is a real-time recommendation engine that can operate within an e-commerce platform. It encompasses ETL processes, a Q mechanism, and Time Series databases. It operates with a Docker-compose file. To initiate, type the following command:

```bash
docker-compose up -d --build
```
<br>

## Architecture

<br><br>

![Architecture](/Documantation/Drawings/product_match.png)


This platform reads products from a JSON file, sends them to Kafka first, and then stores them in a time series database. ETL processes manage the data flow between PostgreSQL and Cassandra. Django exposes recommended data through API services. All services run within Docker containers.


All services include their own init scripts. There is **no need to create tables or configure anything** in any database. These processes occur during the initial build of the containers.

<br>

### Cassandra

Cassandra contains 2 tables. One of the tables contains visited products, while the other contains orders. Their names are *product_views* and *order_views*.


*Keyspace = productviews* 


**product_views**

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
| - messageid TEXT - | - event TEXT - - - | - userid TEXT - - - - - - 
| - productid TEXT - | - source TEXT - - -| - messagetime TIMESTAMP - |
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


**order_views**

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
| - orderid TEXT - - | - productid TEXT - | - categoryid TEXT - - - 
| - quantity INT - - | - userid TEXT - - -| - messagetime TIMESTAMP |
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

<br>

### Airflow

Airflow operates with all initialization configurations. Both scheduling settings and the web server come active. Additionally, the Python file that will manage ETL processes is included and starts running when the container is up.


Navigate to the following URL for the Airflow web server interface:

```http://localhost:8080/login/```

Username: airflow
Password: airflow

You can manage your ETL processes from this interface.

<br>

### Kafka

Kafka is the pipeline that transfers the click data it reads to the database. Here, the queued data arrives at the container responsible for loading data into Cassandra.

<br>

### Django


Default Django URL: 

```http://localhost:8000/api/v1/```

<br>

Django contains two endpoints facilitating the retrieval of recommendation data. They are as follows:

**/api/{{api_version}}/user_nav_history_latest_products/** *(HTTP: GET, DELETE)*

**GET Method**
- Returns the last 10 products from my browsing history, sorted by viewing date.
- Receives the "user-id" parameter in the header and returns a JSON with "user-id", "products", and "type" keys. "products" returns 10 different product recommendations.

**DELETE Method**
- Receives the "user-id" and "product-id" parameters in the header.

<br>

**/api/{{api_version}}/user_history_recommendations/** *(HTTP: GET)*

**GET Method**
- Understands a user's interest based on browsing history items and recommends 10 products. If the user has no browsing history, returns the top-selling products of the previous month.
Receives the "user-id" parameter in the header and returns a JSON with "user-id", "products", and "type" keys. "products" returns 10 different product recommendations.

<br>

### PostgreSQL

![PostgreSQL_Tables](/Documantation/Drawings/postgresql_tables.png)

During the ETL process, data is extracted from PostgreSQL. There are 3 tables in PostgreSQL as shown in the diagram. Additionally, PostgreSQL also stores Django data in a separate database.

<br><br>

## Test And Development

<br>

### Devcontainer 

All containers contain devcontainer files, enabling remote connections from within VSCode. No additional effort is needed for testing and new developments. To start the devcontainer, first install the devcontainer extension in the VSCode application. Then follow these steps:

- Open the Command Palette: Press Ctrl+Shift+P (Windows/Linux) or Cmd+Shift+P (Mac) to open the Command Palette.
- Open the Devcontainer: Search for the "Remote-Containers: Open Folder in Container" command in the Command Palette and select it. This command will open the relevant service in the devcontainer.

<br>

### Postman Collections



The Postman collections for testing API endpoints are available within the repository. The folder structure is as follows:


```/Documantation/Postman```


You can find the Postman collections in the "Postman" folder located within the "Documentation" directory of the repository.

<br>

### Test Data Generator



This service located in the ```/Test``` folder is responsible for generating data during unit tests and loading it into PostgreSQL. Afterwards, the generated data can be loaded into Cassandra through ETL processes. This way, data suitable for querying from endpoints can be obtained by testing PostgreSQL configurations, ETL processes, Airflow, and Cassandra tables.

-The generated data is stored according to the PK and REF structure.
-To migrate the generated data to Cassandra, a DAG must be triggered in Airflow.



<br><br><br><br><br><br>


