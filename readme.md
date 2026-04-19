# Proyecto Escuela: Pipeline Airflow y Aplicación MVC

Este proyecto implementa un sistema integral de gestión educativa bajo el patrón Modelo-Vista-Controlador (MVC), automatizado mediante flujos de datos (DAGs) en Apache Airflow para la población de datos en PostgreSQL y SQLite.

El sistema destaca por su enfoque en **Bases de Datos Avanzadas**, utilizando transacciones seguras con bloqueos de fila y un sistema de auditoría basado en disparadores (triggers).

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
| `dinero` | FLOAT | NOT NULL (Saldo para matrículas) |

### 1.3. Tabla: Cursos
| Columna | Tipo de dato | Restricciones |
| :--- | :--- | :--- |
| `id_curso` | SERIAL | PRIMARY KEY |
| `nombre_curso` | VARCHAR(100) | NOT NULL |
| `id_profesor` | INTEGER | FK → `profesores(id_profesor)` (ON DELETE CASCADE) |
| `capacidad_max` | INTEGER | NOT NULL (Límite de alumnos) |
| `precio` | FLOAT | NOT NULL |

### 1.4. Tabla: Matrículas (Relación N:M)
| Columna | Tipo de dato | Restricciones |
| :--- | :--- | :--- |
| `id_alumno` | INTEGER | FK → `alumnos(id_alumno)` (ON DELETE CASCADE) |
| `id_curso` | INTEGER | FK → `cursos(id_curso)` (ON DELETE CASCADE) |
| **PK Compuesta** | | `PRIMARY KEY (id_alumno, id_curso)` |

---

## 2. Lógica Avanzada de Base de Datos

### 2.1. Sistema de Auditoría (Triggers)
Se han implementado tablas de auditoría (`audit_profesores`, `audit_alumnos`, `audit_cursos`) y funciones en **PL/pgSQL** para rastrear cada operación (INSERT, UPDATE, DELETE). Esto garantiza que, incluso si se elimina un registro, quede constancia de quién realizó la acción y qué datos existían previamente.

### 2.2. Matriculación Transaccional
El proceso de inscripción de alumnos no es una simple inserción; se ha diseñado como una **transacción ACID** que incluye:
1. **Bloqueo de Filas (`FOR UPDATE`)**: Evita condiciones de carrera en el saldo y cupos.
2. **Validación de Cupo**: Verifica que existan plazas disponibles.
3. **Validación de Saldo**: Comprueba que el alumno tenga dinero suficiente.
4. **Atomicidad**: Se descuenta el dinero y se crea la matrícula simultáneamente; si algo falla, se aplica un `ROLLBACK`.

---

## 3. Mapa de Rutas de la Aplicación (Endpoints)

| Endpoint | Métodos | Regla (URL) | Descripción |
| :--- | :--- | :--- | :--- |
| **Main** | | | |
| `main.index` | GET | `/` | Página de inicio. |
| **Auth** | | | |
| `auth.login` | GET, POST | `/auth/login` | Acceso al sistema. |
| `auth.logout` | POST | `/auth/logout` | Salida del sistema. |
| **Alumnos** | | | |
| `alumnos.list_` | GET | `/alumnos` | Listado y saldos. |
| `alumnos.new_alumno` | GET, POST | `/alumnos/nuevo` | Registro de alumno. |
| `alumnos.edit_alumno` | GET, POST | `/alumnos/modificar/<id>` | Actualizar datos/dinero. |
| `alumnos.eliminar_alumno` | GET, POST | `/alumnos/eliminar/<id>` | Baja de alumno. |
| `alumnos.auditoria_alumnos` | GET | `/alumnos/auditoria` | Log de cambios. |
| **Profesores** | | | |
| `profesores.list_` | GET | `/profesores` | Listado de docentes. |
| `profesores.new_profesor` | GET, POST | `/profesores/nuevo` | Registro de docente. |
| `profesores.auditoria_profesores` | GET | `/profesores/auditoria` | Log de cambios. |
| **Cursos** | | | |
| `cursos.list_` | GET | `/cursos` | Catálogo y precios. |
| `cursos.new_curso` | GET, POST | `/cursos/nuevo` | Crear asignatura. |
| `cursos.auditoria_cursos` | GET | `/cursos/auditoria` | Historial de precios/cupos. |
| **Matrículas** | | | |
| `matriculas.list_` | GET | `/matriculas` | Ver inscripciones actuales. |
| `matriculas.matricular_alumno` | GET, POST | `/matriculas/nuevo` | **Proceso Transaccional**. |
| `matriculas.demo_rollback` | GET | `/matriculas/demo-rollback` | Test de integridad. |

---

## 4. Requisitos Previos

- **Lenguaje:** Python v3.12.3
- **Base de Datos:** PostgreSQL v16.13 y SQLite
- **Sistema Operativo:** Ubuntu 24.04 LTS / Windows 10

---

## 5. Estructura del Proyecto

### 5.1. Aplicación MVC
- `app.py`: Punto de entrada de Flask.
- `models/`: Lógica de acceso a datos y entidades.
- `routes/`: Definición de Blueprints y controladores.
- `templates/`: Vistas HTML (Jinja2).

### 5.2. Airflow (Orquestación)
- `mi_primer_dag.py`: DAG principal de orquestación.
- `dag_sqlite.py`: Gestión de datos en SQLite.
- `insert_data.py`: Scripts de carga masiva automatizada.

---

## 6. Configuración y Despliegue

### Airflow
1. Instalar dependencias: `pip install -r requirements_airflow.txt`
2. Configurar `.env` con credenciales de PostgreSQL.
3. Iniciar: `airflow standalone`

### Aplicación MVC
1. Instalar dependencias: `pip install -r requirements_mvc.txt`
2. Ejecutar: `flask run`
3. Acceso: `http://localhost:5000`

---

## 7. Credenciales y Acceso
- **Base de Datos:** Usuario definido en `database.ini` y `.env`.
- **App Web:** El sistema permite el acceso mediante correos generados por el DAG de carga masiva.