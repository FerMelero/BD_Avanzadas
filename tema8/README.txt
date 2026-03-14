# DAGs de ejemplo para Apache Airflow

Contenido:
- `postgres_pipeline_secuencial.py`: versión lineal del flujo.
- `postgres_pipeline_paralelo.py`: versión con ramas paralelas tras la carga inicial.

## Scripts esperados
Estos DAGs asumen que los scripts están en:

`/opt/airflow/dags/scripts/`

con estos nombres:
- `00_check_connection.py`
- `01_create_schema.py`
- `02_insert_rows.py`
- `03_select_rows.py`
- `04_update_rows.py`
- `05_delete_rows.py`
- `06_transactions.py`
- `07_pooling.py`

## Uso
1. Copia los archivos `.py` de este zip a la carpeta de DAGs de Airflow.
2. Copia tus scripts a `/opt/airflow/dags/scripts/`.
3. Reinicia o deja que el scheduler recargue los DAGs.
4. Lanza el DAG desde la interfaz web.

## Nota didáctica
La versión paralela está pensada para enseñar:
- dependencias
- concurrencia
- sincronización final
- observación de estados en la UI
