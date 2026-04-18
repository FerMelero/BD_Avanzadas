from __future__ import annotations

import psycopg

from config import load_config




DDL = (
    # Profesores
    '''CREATE TABLE IF NOT EXISTS profesores (
        id_profesor SERIAL PRIMARY KEY,
        nombre VARCHAR(100) NOT NULL,
        apellido VARCHAR(100) NOT NULL,
        fecha_nacimiento DATE NOT NULL,
        dni VARCHAR(20) NOT NULL UNIQUE
    );''',

    # Alumnos
    '''CREATE TABLE IF NOT EXISTS alumnos (
        id_alumno SERIAL PRIMARY KEY,
        nombre VARCHAR(100) NOT NULL,
        apellido VARCHAR(100) NOT NULL,
        fecha_nacimiento DATE NOT NULL,
        dni VARCHAR(20) NOT NULL UNIQUE,
        dinero FLOAT NOT NULL
    );''',

    # Cursos (1 profesor por curso)
    '''CREATE TABLE IF NOT EXISTS cursos (
        id_curso SERIAL PRIMARY KEY,
        nombre_curso VARCHAR(100) NOT NULL,
        id_profesor INTEGER NOT NULL,
        capacidad_max INTEGER NOT NULL,
        precio FLOAT NOT NULL,
        FOREIGN KEY (id_profesor)
            REFERENCES profesores (id_profesor)
            ON UPDATE CASCADE
            ON DELETE CASCADE
    );''',

    # Matrículas (N:M entre alumnos y cursos)
    '''CREATE TABLE IF NOT EXISTS matriculas (
        id_alumno INTEGER NOT NULL,
        id_curso INTEGER NOT NULL,
        PRIMARY KEY (id_alumno, id_curso),
        FOREIGN KEY (id_alumno)
            REFERENCES alumnos (id_alumno)
            ON UPDATE CASCADE
            ON DELETE CASCADE,
        FOREIGN KEY (id_curso)
            REFERENCES cursos (id_curso)
            ON UPDATE CASCADE
            ON DELETE CASCADE
    );''',                         
    '''
    CREATE TABLE IF NOT EXISTS audit_profesores(
    operacion      CHAR(1) NOT NULL,
    stamp          TIMESTAMP NOT NULL,
    user_id        VARCHAR(100) NOT NULL,
    nombre_profesor VARCHAR(100) NOT NULL,
    id_profesor    INTEGER,
    dni_profesor   VARCHAR(20)
);''',
'''

CREATE TABLE IF NOT EXISTS audit_alumnos(
    operacion      CHAR(1) NOT NULL,
    stamp          TIMESTAMP NOT NULL,
    user_id        VARCHAR(100) NOT NULL,
    nombre_alumno  VARCHAR(100) NOT NULL,
    id_alumno      INTEGER,
    dni_alumno     VARCHAR(20)
);''',

'''
CREATE TABLE IF NOT EXISTS audit_cursos(
    operacion      CHAR(1) NOT NULL,
    stamp          TIMESTAMP NOT NULL,
    user_id        VARCHAR(100) NOT NULL,
    nombre_curso   VARCHAR(100) NOT NULL,
    id_curso       INTEGER,
    precio_curso   FLOAT
);
''',

'''
CREATE OR REPLACE FUNCTION fn_audit_profesores()
RETURNS TRIGGER AS $$
BEGIN
    IF (TG_OP = 'DELETE') THEN
        INSERT INTO audit_profesores(operacion, stamp, user_id, nombre_profesor, id_profesor, dni_profesor)
        VALUES ('D', now(), current_user, OLD.nombre, OLD.id_profesor, OLD.dni);
        RETURN OLD;
    ELSIF (TG_OP = 'UPDATE') THEN
        INSERT INTO audit_profesores(operacion, stamp, user_id, nombre_profesor, id_profesor, dni_profesor)
        VALUES ('U', now(), current_user, NEW.nombre, NEW.id_profesor, NEW.dni);
        RETURN NEW;
    ELSIF (TG_OP = 'INSERT') THEN
        INSERT INTO audit_profesores(operacion, stamp, user_id, nombre_profesor, id_profesor, dni_profesor)
        VALUES ('I', now(), current_user, NEW.nombre, NEW.id_profesor, NEW.dni);
        RETURN NEW;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tr_audit_profesores
AFTER INSERT OR UPDATE OR DELETE ON profesores
FOR EACH ROW EXECUTE FUNCTION fn_audit_profesores();
''',

'''
CREATE OR REPLACE FUNCTION fn_audit_alumnos()
RETURNS TRIGGER AS $$
BEGIN
    IF (TG_OP = 'DELETE') THEN
        INSERT INTO audit_alumnos(operacion, stamp, user_id, nombre_alumno, id_alumno, dni_alumno)
        VALUES ('D', now(), current_user, OLD.nombre, OLD.id_alumno, OLD.dni);
        RETURN OLD;
    ELSIF (TG_OP = 'UPDATE') THEN
        INSERT INTO audit_alumnos(operacion, stamp, user_id, nombre_alumno, id_alumno, dni_alumno)
        VALUES ('U', now(), current_user, NEW.nombre, NEW.id_alumno, NEW.dni);
        RETURN NEW;
    ELSIF (TG_OP = 'INSERT') THEN
        INSERT INTO audit_alumnos(operacion, stamp, user_id, nombre_alumno, id_alumno, dni_alumno)
        VALUES ('I', now(), current_user, NEW.nombre, NEW.id_alumno, NEW.dni);
        RETURN NEW;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tr_audit_alumnos
AFTER INSERT OR UPDATE OR DELETE ON alumnos
FOR EACH ROW EXECUTE FUNCTION fn_audit_alumnos();
''',

'''
CREATE OR REPLACE FUNCTION fn_audit_cursos()
RETURNS TRIGGER AS $$
BEGIN
    IF (TG_OP = 'DELETE') THEN
        INSERT INTO audit_cursos(operacion, stamp, user_id, nombre_curso, id_curso, precio_curso)
        VALUES ('D', now(), current_user, OLD.nombre_curso, OLD.id_curso, OLD.precio);
        RETURN OLD;
    ELSIF (TG_OP = 'UPDATE') THEN
        INSERT INTO audit_cursos(operacion, stamp, user_id, nombre_curso, id_curso, precio_curso)
        VALUES ('U', now(), current_user, NEW.nombre_curso, NEW.id_curso, NEW.precio);
        RETURN NEW;
    ELSIF (TG_OP = 'INSERT') THEN
        INSERT INTO audit_cursos(operacion, stamp, user_id, nombre_curso, id_curso, precio_curso)
        VALUES ('I', now(), current_user, NEW.nombre_curso, NEW.id_curso, NEW.precio);
        RETURN NEW;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tr_audit_cursos
AFTER INSERT OR UPDATE OR DELETE ON cursos
FOR EACH ROW EXECUTE FUNCTION fn_audit_cursos();
'''

)

def create_tables() -> None:
    """Create demo tables for the lab (idempotent)."""
    cfg = load_config()
    with psycopg.connect(**cfg) as conn:
        with conn.cursor() as cur:
            for stmt in DDL:
                cur.execute(stmt)
    print("Tables created (or already existed).")


if __name__ == "__main__":
    create_tables()
