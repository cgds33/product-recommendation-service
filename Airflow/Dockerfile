FROM apache/airflow:2.0.1

ENV AIRFLOW__CORE__EXECUTOR=LocalExecutor
ENV AIRFLOW__CORE__SQL_ALCHEMY_CONN=postgresql+psycopg2://postgres:123456@postgresdb:5432/airflow
ENV AIRFLOW__CORE__FERNET_KEY=FB0o_zt4e3Ziq3LdUUO7F2Z95cvFFx16hU8jTeR1ASM=
ENV AIRFLOW__CORE__LOAD_EXAMPLES=False
ENV AIRFLOW__CORE__LOGGING_LEVEL=INFO

USER root

RUN apt-get update \
  && apt-get install -y --no-install-recommends \
         vim \
  && apt-get autoremove -yqq --purge \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

COPY --chown=airflow:root /dags/pm_dag.py /opt/airflow/dags
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

USER airflow