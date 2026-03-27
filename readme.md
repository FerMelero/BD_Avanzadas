# Proyecto Escuela: Pipeline Airflow y Aplicación MVC

Este proyecto implementa un sistema integral de gestión educativa bajo el patrón Modelo-Vista-Controlador (MVC), automatizado mediante flujos de datos (DAGs) en Apache Airflow para la población de datos en PostgreSQL y SQLite.

---

## 1. Estructura de la Base de Datos

El sistema utiliza un modelo relacional para gestionar la información académica. Las relaciones están diseñadas para mantener la integridad referencial mediante eliminaciones en cascada.

### 1.1. Tabla: Profesores
| Columna | Tipo de dato | Restricciones |
| :--- | :--- | :--- |
| `id_profesor` | SERIAL | PRIMARY KEY |
| `nombre` | VARCHAR(100) | NOT NULL |
| `apellido` | VARCHAR(100) | NOT NULL |
| `fecha_nacimiento` | DATE | NOT NULL |
| `dni` | VARCHAR(20) | NOT NULL, UNIQUE |

### 1.2. Tabla: Alumnos
| Columna | Tipo de dato | Restricciones |
| :--- | :--- | :--- |
| `id_alumno` | SERIAL | PRIMARY KEY |
| `nombre` | VARCHAR(100) | NOT NULL |
| `apellido` | VARCHAR(100) | NOT NULL |
| `fecha_nacimiento` | DATE | NOT NULL |
| `dni` | VARCHAR(20) | NOT NULL, UNIQUE |

### 1.3. Tabla: Cursos
| Columna | Tipo de dato | Restricciones |
| :--- | :--- | :--- |
| `id_curso` | SERIAL | PRIMARY KEY |
| `nombre_curso` | VARCHAR(100) | NOT NULL |
| `id_profesor` | INTEGER | FK → `profesores(id_profesor)` (ON DELETE CASCADE) |

### 1.4. Tabla: Matrículas (Relación N:M)
| Columna | Tipo de dato | Restricciones |
| :--- | :--- | :--- |
| `id_alumno` | INTEGER | FK → `alumnos(id_alumno)` (ON DELETE CASCADE) |
| `id_curso` | INTEGER | FK → `cursos(id_curso)` (ON DELETE CASCADE) |
| **PK Compuesta** | | `PRIMARY KEY (id_alumno, id_curso)` |

---

## 2. Requisitos Previos

- **Lenguaje:** Python v3.12.3
- **Base de Datos:** PostgreSQL v16.13 y SQLite
- **Sistema Operativo:** Ubuntu 24.04 LTS / Windows 10
- **Entorno:** Se requiere el uso de entornos virtuales para la separación de dependencias de Airflow y la App MVC.

---

## 3. Estructura del Proyecto

### 3.1. Aplicación MVC
- `app.py`: Punto de entrada de Flask.
- `models/`: Lógica de acceso a datos.
- `routes/`: Definición de endpoints.
- `templates/`: Archivos HTML.
- `database.ini`: Configuración de conexión.
- `bd_sqlite/`: Directorio para la base de datos local.

### 3.2. Airflow (Orquestación)
- `mi_primer_dag.py`: DAG principal de orquestación.
- `dag_sqlite.py`: DAG para la gestión de datos en SQLite.
- `connect.py`: Utilidad de validación de conexión.
- `insert_data.py` / `insert.py`: Scripts de carga masiva.
- `config.py`: Gestor de carga de parámetros.
- `.env`: Variables de entorno sensibles.

---

## 4. Configuración y Despliegue de Airflow

### Paso 1: Instalación
pip install -r requirements_airflow.txt

### Paso 2: Configuración de Entorno

Es obligatorio configurar el archivo .env en la carpeta de los DAGs con los siguientes parámetros:

    Credenciales de PostgreSQL (Host, User, Pass, DB).

    Ruta absoluta para la base de datos SQLite.

### Paso 3: Ejecución
Bash

airflow standalone

Acceda a la interfaz web en: http://localhost:8080
### Paso 4: Ejecución de DAGs

    check_postgres_connection: Ejecutar primero para validar conectividad.

    escuela_postgres_dag: Ejecutar para realizar el flujo completo:

        Validación.

        Creación de tablas.

        Inserción de registros.

## 5. Ejecución de la Aplicación MVC
### Paso 1: Instalación

pip install -r requirements_mvc.txt

### Paso 2: Lanzamiento


`flask run`

La aplicación estará disponible en: http://localhost:5000
## 6. Credenciales de Acceso
### 6.1. Acceso a Base de Datos

    Usuario: user_practicas

    Configuración: Definida en database.ini y archivo .env.

### 6.2. Acceso a Aplicación Web

El sistema permite el acceso mediante cualquier correo electrónico de Alumno o Profesor generado automáticamente durante la ejecución del DAG de SQLite. Consulte los logs de inserción para obtener una lista de correos válidos.