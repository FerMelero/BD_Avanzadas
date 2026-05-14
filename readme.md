# Aplicacion Web Flask - Gestion Academica

Aplicacion web desarrollada con Flask y PostgreSQL para la gestion de alumnos, profesores, asignaturas y matriculas. Incluye soporte para datos geograficos mediante PostGIS, busqueda difusa con `pg_trgm`, auditoria de cambios mediante triggers y gestion de transacciones.

---

## Requisitos previos

- Python 3.10 o superior
- PostgreSQL con las extensiones `pg_trgm`, `unaccent` y `postgis`
- pip

---

## Instalacion

### 1. Clonar el repositorio

```bash
git clone https://github.com/FerMelero/BD_Avanzadas.git
cd <nombre-del-proyecto>
```

### 2. Crear el entorno virtual

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux / macOS:**
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar la base de datos

Crea un archivo `database.ini` con las credenciales de tu base de datos PostgreSQL. Despues ejecuta el script de inicializacion `create_tables.py`para crear las tablas, indices, triggers y vistas:

```bash
python create_tables.py
```

### 5. Ejecutar la aplicacion

```bash
flask run
```

---

## Estructura de la base de datos

El esquema esta compuesto por las siguientes tablas principales y tablas de auditoria:

### Tablas principales

| Tabla | Descripcion |
|---|---|
| `profesores` | Datos personales de los profesores (nombre, apellido, fecha de nacimiento, DNI) |
| `alumnos` | Datos personales de los alumnos, incluyendo saldo (`dinero`) |
| `asignaturas` | Asignaturas con nombre multiidioma en JSONB, profesor asignado, capacidad maxima y precio |
| `matriculas` | Relacion muchos a muchos entre alumnos y asignaturas |
| `alumno_ubicaciones` | Ubicacion geografica de cada alumno (punto PostGIS, SRID 4326) |
| `asignatura_poligonos` | Area geografica asociada a cada asignatura (poligono PostGIS, SRID 4326) |

### Tablas de auditoria

| Tabla | Descripcion |
|---|---|
| `audit_profesores` | Registro de INSERT, UPDATE y DELETE sobre `profesores` |
| `audit_alumnos` | Registro de INSERT, UPDATE y DELETE sobre `alumnos` |
| `audit_asignaturas` | Registro de INSERT, UPDATE y DELETE sobre `asignaturas` |

Cada tabla de auditoria almacena la operacion realizada (`I`, `U`, `D`), la marca de tiempo, el usuario de base de datos y los valores afectados.

### Vistas

| Vista | Descripcion |
|---|---|
| `vista_alumnos_profesores_asignaturas` | Cruza matriculas, alumnos, asignaturas y profesores para mostrar nombre del alumno, nombre del profesor y nombre de la asignatura en espanol |

### Indices destacados

- Indice GIN sobre `asignaturas.nombres_multi` para busquedas JSONB.
- Indices GIST con `pg_trgm` sobre los nombres en espanol e ingles de las asignaturas para busqueda difusa sin tildes.
- Indices GIST sobre las geometrias de ubicaciones y poligonos para consultas espaciales.

---

## Rutas de la aplicacion

### Autenticacion (`/auth`)

| Metodo | Ruta | Descripcion |
|---|---|---|
| GET, POST | `/auth/login` | Formulario de inicio de sesion |
| POST | `/auth/logout` | Cierre de sesion |

### Pagina principal

| Metodo | Ruta | Descripcion |
|---|---|---|
| GET | `/` | Pagina de inicio |

### Alumnos (`/alumnos`)

| Metodo | Ruta | Descripcion |
|---|---|---|
| GET | `/alumnos` | Listado de todos los alumnos |
| GET, POST | `/alumnos/nuevo` | Crear un nuevo alumno |
| GET | `/alumnos/<id_alumno>` | Ver detalle de un alumno |
| GET, POST | `/alumnos/modificar/<id_alumno>` | Editar datos de un alumno |
| GET, POST | `/alumnos/eliminar/<id_alumno>` | Eliminar un alumno |
| GET, POST | `/alumnos/<id_alumno>/editar-ubicacion` | Asignar o modificar la ubicacion geografica del alumno |
| GET, POST | `/alumnos/<id_alumno>/viajar` | Simular el desplazamiento del alumno a una nueva ubicacion |
| GET | `/alumnos/auditoria` | Consultar el historial de auditoria de alumnos |

### Profesores (`/profesores`)

| Metodo | Ruta | Descripcion |
|---|---|---|
| GET | `/profesores` | Listado de todos los profesores |
| GET, POST | `/profesores/nuevo` | Crear un nuevo profesor |
| GET | `/profesores/<id_profesor>` | Ver detalle de un profesor |
| GET, POST | `/profesores/modificar/<id_profesor>` | Editar datos de un profesor |
| GET, POST | `/profesores/eliminar/<id_profesor>` | Eliminar un profesor |
| GET | `/profesores/asignaturasCaros/<id_profesor>` | Ver las asignaturas mas caras asociadas a un profesor |
| GET | `/profesores/auditoria` | Consultar el historial de auditoria de profesores |

### Asignaturas (`/asignaturas`)

| Metodo | Ruta | Descripcion |
|---|---|---|
| GET | `/asignaturas` | Listado de todas las asignaturas |
| GET, POST | `/asignaturas/nuevo` | Crear una nueva asignatura |
| GET | `/asignaturas/<id_asignatura>` | Ver detalle de una asignatura |
| GET, POST | `/asignaturas/modificar/<id_asignatura>` | Editar datos de una asignatura |
| GET, POST | `/asignaturas/eliminar/<id_asignatura>` | Eliminar una asignatura |
| GET, POST | `/asignaturas/<id_asignatura>/editar-poligono` | Asignar o modificar el area geografica de la asignatura |
| GET | `/asignaturas/dinero` | Consultar el balance economico relacionado con asignaturas |
| GET | `/asignaturas/estadisticas-precios` | Ver estadisticas de precios de las asignaturas |
| GET | `/asignaturas/reporte-capacidades` | Reporte de ocupacion y capacidad maxima por asignatura |
| GET | `/asignaturas/auditoria` | Consultar el historial de auditoria de asignaturas |

### Matriculas (`/matriculas`)

| Metodo | Ruta | Descripcion |
|---|---|---|
| GET | `/matriculas` | Listado de todas las matriculas |
| GET, POST | `/matriculas/nuevo` | Matricular un alumno en una asignatura |
| GET | `/matriculas/vista` | Vista cruzada de matriculas con nombres de alumnos, profesores y asignaturas |
| GET | `/matriculas/demo-rollback` | Demostracion de rollback de transaccion |

---

## Caracteristicas tecnicas

- **Auditoria automatica**: triggers en PostgreSQL registran cada INSERT, UPDATE y DELETE sobre las tablas principales.
- **Datos geograficos**: soporte PostGIS para almacenar y consultar ubicaciones de alumnos y areas de asignaturas.
- **Busqueda difusa**: indices GIST con `pg_trgm` y `unaccent` permiten busquedas aproximadas insensibles a tildes.
- **Nombres multiidioma**: la columna `nombres_multi` de asignaturas es de tipo JSONB, permitiendo almacenar el nombre en multiples idiomas (por ejemplo, `{"es": "Matematicas", "en": "Mathematics"}`).
- **Gestion de transacciones**: se incluye una ruta de demostracion de rollback para ilustrar el control de transacciones en PostgreSQL.