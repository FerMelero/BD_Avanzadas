from __future__ import annotations
import psycopg
from config import load_config
DDL = (
    '''DROP VIEW IF EXISTS vista_alumnos_profesores_cursos CASCADE;''',
    '''DROP TABLE IF EXISTS matriculas CASCADE;''',
    '''DROP TABLE IF EXISTS cursos CASCADE;''',
    '''DROP TABLE IF EXISTS alumnos CASCADE;''',
    '''DROP TABLE IF EXISTS profesores CASCADE;''',
    '''DROP TABLE IF EXISTS audit_profesores CASCADE;''',
    '''DROP TABLE IF EXISTS audit_alumnos CASCADE;''',
    '''DROP TABLE IF EXISTS audit_cursos CASCADE;''',

    '''CREATE EXTENSION IF NOT EXISTS pg_trgm SCHEMA public;''',
    '''CREATE EXTENSION IF NOT EXISTS unaccent SCHEMA public;''',

    '''CREATE OR REPLACE FUNCTION unaccent_immutable(text)
    RETURNS text AS $$
        SELECT public.unaccent($1);
    $$ LANGUAGE sql IMMUTABLE PARALLEL SAFE;''',

    
    # Tabla Profesores
    '''CREATE TABLE profesores (
        id_profesor SERIAL PRIMARY KEY,
        nombre VARCHAR(100) NOT NULL,
        apellido VARCHAR(100) NOT NULL,
        fecha_nacimiento DATE NOT NULL,
        dni VARCHAR(20) NOT NULL UNIQUE
    );''',

    # Tabla Alumnos
    '''CREATE TABLE alumnos (
        id_alumno SERIAL PRIMARY KEY,
        nombre VARCHAR(100) NOT NULL,
        apellido VARCHAR(100) NOT NULL,
        fecha_nacimiento DATE NOT NULL,
        dni VARCHAR(20) NOT NULL UNIQUE,
        dinero FLOAT NOT NULL
    );''',

    # Tabla Cursos
    '''CREATE TABLE cursos (
        id_curso SERIAL PRIMARY KEY,
        nombres_multi JSONB NOT NULL,
        id_profesor INTEGER NOT NULL REFERENCES profesores(id_profesor) ON DELETE CASCADE,
        capacidad_max INTEGER NOT NULL,
        precio FLOAT NOT NULL
    );''',

    # Matrículas
    '''CREATE TABLE matriculas (
        id_alumno INTEGER NOT NULL REFERENCES alumnos(id_alumno) ON DELETE CASCADE,
        id_curso INTEGER NOT NULL REFERENCES cursos(id_curso) ON DELETE CASCADE,
        PRIMARY KEY (id_alumno, id_curso)
    );''',

    # auditoria
    '''CREATE TABLE audit_cursos(
        operacion CHAR(1), stamp TIMESTAMP, user_id VARCHAR(100), 
        id_curso INTEGER, nombres_multi JSONB, id_profesor INTEGER, 
        capacidad_max INTEGER, precio FLOAT
    );''',

    '''CREATE TABLE IF NOT EXISTS audit_profesores(
        operacion       CHAR(1) NOT NULL,
        stamp           TIMESTAMP NOT NULL,
        user_id         VARCHAR(100) NOT NULL,
        id_profesor     INTEGER,
        nombre          VARCHAR(100),
        apellido        VARCHAR(100),
        fecha_nacimiento DATE,
        dni             VARCHAR(20)
    );''',

    '''CREATE TABLE IF NOT EXISTS audit_alumnos(
        operacion       CHAR(1) NOT NULL,
        stamp           TIMESTAMP NOT NULL,
        user_id         VARCHAR(100) NOT NULL,
        id_alumno       INTEGER,
        nombre          VARCHAR(100),
        apellido        VARCHAR(100),
        fecha_nacimiento DATE,
        dni             VARCHAR(20),
        dinero          FLOAT
    );''',

    '''CREATE OR REPLACE FUNCTION fn_audit_cursos() RETURNS TRIGGER AS $$
    DECLARE r record;
    BEGIN
        r := CASE WHEN (TG_OP = 'DELETE') THEN OLD ELSE NEW END;
        INSERT INTO audit_cursos VALUES (SUBSTR(TG_OP, 1, 1), now(), current_user, 
        r.id_curso, r.nombres_multi, r.id_profesor, r.capacidad_max, r.precio);
        RETURN r;
    END; $$ LANGUAGE plpgsql;''',

    '''CREATE TRIGGER tr_audit_cursos AFTER INSERT OR UPDATE OR DELETE ON cursos
       FOR EACH ROW EXECUTE FUNCTION fn_audit_cursos();''',

    # 6. VISTA
    '''CREATE VIEW vista_alumnos_profesores_cursos AS
    SELECT a.nombre || ' ' || a.apellido AS nombre_alumno,
           p.nombre || ' ' || p.apellido AS nombre_profesor,
           c.nombres_multi->>'es' AS nombre_curso
    FROM matriculas m
    JOIN alumnos a ON m.id_alumno = a.id_alumno
    JOIN cursos c ON m.id_curso = c.id_curso
    JOIN profesores p ON c.id_profesor = p.id_profesor;''',

    # ÍNDICES 
    
    '''CREATE INDEX idx_cursos_nombres_jsonb ON cursos USING GIN (nombres_multi);''',
    
    '''CREATE INDEX idx_cursos_fuzzy_es ON cursos 
       USING gist (unaccent_immutable(nombres_multi->>'es') gist_trgm_ops);''',
    
    '''CREATE INDEX idx_cursos_fuzzy_en ON cursos 
       USING gist (unaccent_immutable(nombres_multi->>'en') gist_trgm_ops);''',

    '''CREATE INDEX idx_alumnos_nombre ON alumnos (nombre);''',
    '''CREATE INDEX idx_profesores_nombre ON profesores (nombre);'''
)

def create_tables() -> None:
    cfg = load_config()
    with psycopg.connect(**cfg) as conn:
        with conn.cursor() as cur:
            for stmt in DDL:
                cur.execute(stmt)
    print("Base de datos configurada correctamente (Tablas, Vistas, Auditoría e Índices).")

if __name__ == "__main__":
    create_tables()