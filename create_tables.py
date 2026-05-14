from __future__ import annotations
import psycopg
from config import load_config

DDL = (
    '''DROP VIEW IF EXISTS vista_alumnos_profesores_asignaturas CASCADE;''',
    '''DROP TABLE IF EXISTS matriculas CASCADE;''',
    '''DROP TABLE IF EXISTS asignaturas CASCADE;''',
    '''DROP TABLE IF EXISTS alumnos CASCADE;''',
    '''DROP TABLE IF EXISTS profesores CASCADE;''',
    '''DROP TABLE IF EXISTS audit_profesores CASCADE;''',
    '''DROP TABLE IF EXISTS audit_alumnos CASCADE;''',
    '''DROP TABLE IF EXISTS audit_asignaturas CASCADE;''',

    '''CREATE EXTENSION IF NOT EXISTS pg_trgm SCHEMA public;''',
    '''CREATE EXTENSION IF NOT EXISTS unaccent SCHEMA public;''',
    '''CREATE EXTENSION IF NOT EXISTS postgis SCHEMA public;''',

    '''CREATE OR REPLACE FUNCTION unaccent_immutable(text)
    RETURNS text AS $$
        SELECT public.unaccent($1);
    $$ LANGUAGE sql IMMUTABLE PARALLEL SAFE;''',

    '''CREATE TABLE profesores (
        id_profesor SERIAL PRIMARY KEY,
        nombre VARCHAR(100) NOT NULL,
        apellido VARCHAR(100) NOT NULL,
        fecha_nacimiento DATE NOT NULL,
        dni VARCHAR(20) NOT NULL UNIQUE
    );''',

    '''CREATE TABLE alumnos (
        id_alumno SERIAL PRIMARY KEY,
        nombre VARCHAR(100) NOT NULL,
        apellido VARCHAR(100) NOT NULL,
        fecha_nacimiento DATE NOT NULL,
        dni VARCHAR(20) NOT NULL UNIQUE,
        dinero FLOAT NOT NULL
    );''',

    '''CREATE TABLE asignaturas (
        id_asignatura SERIAL PRIMARY KEY,
        nombres_multi JSONB NOT NULL,
        id_profesor INTEGER NOT NULL REFERENCES profesores(id_profesor) ON DELETE CASCADE,
        capacidad_max INTEGER NOT NULL,
        precio FLOAT NOT NULL
    );''',

    '''CREATE TABLE matriculas (
        id_alumno INTEGER NOT NULL REFERENCES alumnos(id_alumno) ON DELETE CASCADE,
        id_asignatura INTEGER NOT NULL REFERENCES asignaturas(id_asignatura) ON DELETE CASCADE,
        PRIMARY KEY (id_alumno, id_asignatura)
    );''',

    '''CREATE TABLE alumno_ubicaciones (
        id_alumno INTEGER PRIMARY KEY REFERENCES alumnos(id_alumno) ON DELETE CASCADE,
        ubicacion geometry(Point,4326)
    );''',

    '''CREATE TABLE asignatura_poligonos (
        id_asignatura INTEGER PRIMARY KEY REFERENCES asignaturas(id_asignatura) ON DELETE CASCADE,
        area geometry(Polygon,4326)
    );''',

    '''CREATE INDEX idx_alumno_ubicaciones_geom ON alumno_ubicaciones USING GIST (ubicacion);''',
    '''CREATE INDEX idx_asignatura_poligonos_geom ON asignatura_poligonos USING GIST (area);''',

    '''CREATE TABLE audit_asignaturas(
        operacion CHAR(1),
        stamp TIMESTAMP,
        user_id VARCHAR(100),
        id_asignatura INTEGER,
        nombres_multi JSONB,
        id_profesor INTEGER,
        capacidad_max INTEGER,
        precio FLOAT
    );''',

    '''CREATE TABLE audit_profesores(
        operacion CHAR(1) NOT NULL,
        stamp TIMESTAMP NOT NULL,
        user_id VARCHAR(100) NOT NULL,
        id_profesor INTEGER,
        nombre VARCHAR(100),
        apellido VARCHAR(100),
        fecha_nacimiento DATE,
        dni VARCHAR(20)
    );''',

    '''CREATE TABLE audit_alumnos(
        operacion CHAR(1) NOT NULL,
        stamp TIMESTAMP NOT NULL,
        user_id VARCHAR(100) NOT NULL,
        id_alumno INTEGER,
        nombre VARCHAR(100),
        apellido VARCHAR(100),
        fecha_nacimiento DATE,
        dni VARCHAR(20),
        dinero FLOAT
    );''',

    '''CREATE OR REPLACE FUNCTION fn_audit_asignaturas()
    RETURNS TRIGGER AS $$
    DECLARE
        r RECORD;
    BEGIN
        r := CASE
                WHEN (TG_OP = 'DELETE') THEN OLD
                ELSE NEW
             END;

        INSERT INTO audit_asignaturas
        VALUES (
            SUBSTR(TG_OP, 1, 1),
            now(),
            current_user,
            r.id_asignatura,
            r.nombres_multi,
            r.id_profesor,
            r.capacidad_max,
            r.precio
        );

        RETURN r;
    END;
    $$ LANGUAGE plpgsql;''',

    '''CREATE OR REPLACE FUNCTION fn_audit_profesores()
    RETURNS TRIGGER AS $$
    DECLARE
        r RECORD;
    BEGIN
        r := CASE
                WHEN (TG_OP = 'DELETE') THEN OLD
                ELSE NEW
             END;

        INSERT INTO audit_profesores(
            operacion,
            stamp,
            user_id,
            id_profesor,
            nombre,
            apellido,
            fecha_nacimiento,
            dni
        )
        VALUES (
            SUBSTR(TG_OP,1,1),
            now(),
            current_user,
            r.id_profesor,
            r.nombre,
            r.apellido,
            r.fecha_nacimiento,
            r.dni
        );

        RETURN r;
    END;
    $$ LANGUAGE plpgsql;''',

    '''CREATE OR REPLACE FUNCTION fn_audit_alumnos()
    RETURNS TRIGGER AS $$
    DECLARE
        r RECORD;
    BEGIN
        r := CASE
                WHEN (TG_OP = 'DELETE') THEN OLD
                ELSE NEW
             END;

        INSERT INTO audit_alumnos(
            operacion,
            stamp,
            user_id,
            id_alumno,
            nombre,
            apellido,
            fecha_nacimiento,
            dni,
            dinero
        )
        VALUES (
            SUBSTR(TG_OP,1,1),
            now(),
            current_user,
            r.id_alumno,
            r.nombre,
            r.apellido,
            r.fecha_nacimiento,
            r.dni,
            r.dinero
        );

        RETURN r;
    END;
    $$ LANGUAGE plpgsql;''',

    '''CREATE TRIGGER tr_audit_asignaturas
    AFTER INSERT OR UPDATE OR DELETE
    ON asignaturas
    FOR EACH ROW
    EXECUTE FUNCTION fn_audit_asignaturas();''',

    '''CREATE TRIGGER tr_audit_profesores
    AFTER INSERT OR UPDATE OR DELETE
    ON profesores
    FOR EACH ROW
    EXECUTE FUNCTION fn_audit_profesores();''',

    '''CREATE TRIGGER tr_audit_alumnos
    AFTER INSERT OR UPDATE OR DELETE
    ON alumnos
    FOR EACH ROW
    EXECUTE FUNCTION fn_audit_alumnos();''',

    '''CREATE VIEW vista_alumnos_profesores_asignaturas AS
    SELECT
        a.nombre || ' ' || a.apellido AS nombre_alumno,
        p.nombre || ' ' || p.apellido AS nombre_profesor,
        c.nombres_multi->>'es' AS nombre_asignatura
    FROM matriculas m
    JOIN alumnos a ON m.id_alumno = a.id_alumno
    JOIN asignaturas c ON m.id_asignatura = c.id_asignatura
    JOIN profesores p ON c.id_profesor = p.id_profesor;''',

    '''CREATE INDEX idx_asignaturas_nombres_jsonb
    ON asignaturas USING GIN (nombres_multi);''',

    '''CREATE INDEX idx_asignaturas_fuzzy_es
    ON asignaturas
    USING gist (unaccent_immutable(nombres_multi->>'es') gist_trgm_ops);''',

    '''CREATE INDEX idx_asignaturas_fuzzy_en
    ON asignaturas
    USING gist (unaccent_immutable(nombres_multi->>'en') gist_trgm_ops);''',

    '''CREATE INDEX idx_alumnos_nombre
    ON alumnos (nombre);''',

    '''CREATE INDEX idx_profesores_nombre
    ON profesores (nombre);'''
)

def create_tables() -> None:
    cfg = load_config()

    with psycopg.connect(**cfg) as conn:
        with conn.cursor() as cur:
            for stmt in DDL:
                cur.execute(stmt)

    print("Base de datos configurada correctamente.")

if __name__ == "__main__":
    create_tables()