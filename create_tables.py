from __future__ import annotations
import psycopg
from config import load_config

DDL = (
    '''DROP TABLE IF EXISTS cursos CASCADE;''',
    '''CREATE EXTENSION IF NOT EXISTS unaccent;''',

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

    # Cursos (Actualizado a nombres_multi JSONB para multi-idioma)
    '''CREATE TABLE IF NOT EXISTS cursos (
        id_curso SERIAL PRIMARY KEY,
        nombres_multi JSONB NOT NULL,
        id_profesor INTEGER NOT NULL,
        capacidad_max INTEGER NOT NULL,
        precio FLOAT NOT NULL,
        FOREIGN KEY (id_profesor)
            REFERENCES profesores (id_profesor)
            ON UPDATE CASCADE
            ON DELETE CASCADE
    );''',

    # Matrículas
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

    
    '''DROP VIEW IF EXISTS vista_alumnos_profesores_cursos;''',
    '''CREATE OR REPLACE VIEW vista_alumnos_profesores_cursos AS
    SELECT
        a.nombre || ' ' || a.apellido AS nombre_alumno,
        p.nombre || ' ' || p.apellido AS nombre_profesor,
        c.nombres_multi->>'es' AS nombre_curso
    FROM matriculas m
    JOIN alumnos a ON m.id_alumno = a.id_alumno
    JOIN cursos c ON m.id_curso = c.id_curso
    JOIN profesores p ON c.id_profesor = p.id_profesor;''',


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

    '''CREATE TABLE IF NOT EXISTS audit_cursos(
        operacion       CHAR(1) NOT NULL,
        stamp           TIMESTAMP NOT NULL,
        user_id         VARCHAR(100) NOT NULL,
        id_curso        INTEGER,
        nombres_multi   JSONB,
        id_profesor     INTEGER,
        capacidad_max   INTEGER,
        precio          FLOAT
    );''',


    '''CREATE OR REPLACE FUNCTION fn_audit_profesores()
    RETURNS TRIGGER AS $$
    DECLARE
        r record;
    BEGIN
        r := CASE WHEN (TG_OP = 'DELETE') THEN OLD ELSE NEW END;
        INSERT INTO audit_profesores(operacion, stamp, user_id, id_profesor, nombre, apellido, fecha_nacimiento, dni)
        VALUES (SUBSTR(TG_OP, 1, 1), now(), current_user, r.id_profesor, r.nombre, r.apellido, r.fecha_nacimiento, r.dni);
        RETURN r;
    END;
    $$ LANGUAGE plpgsql;''',

    '''CREATE OR REPLACE FUNCTION fn_audit_alumnos()
    RETURNS TRIGGER AS $$
    DECLARE
        r record;
    BEGIN
        r := CASE WHEN (TG_OP = 'DELETE') THEN OLD ELSE NEW END;
        INSERT INTO audit_alumnos(operacion, stamp, user_id, id_alumno, nombre, apellido, fecha_nacimiento, dni, dinero)
        VALUES (SUBSTR(TG_OP, 1, 1), now(), current_user, r.id_alumno, r.nombre, r.apellido, r.fecha_nacimiento, r.dni, r.dinero);
        RETURN r;
    END;
    $$ LANGUAGE plpgsql;''',

    '''CREATE OR REPLACE FUNCTION fn_audit_cursos()
    RETURNS TRIGGER AS $$
    DECLARE
        r record;
    BEGIN
        r := CASE WHEN (TG_OP = 'DELETE') THEN OLD ELSE NEW END;
        INSERT INTO audit_cursos(operacion, stamp, user_id, id_curso, nombres_multi, id_profesor, capacidad_max, precio)
        VALUES (SUBSTR(TG_OP, 1, 1), now(), current_user, r.id_curso, r.nombres_multi, r.id_profesor, r.capacidad_max, r.precio);
        RETURN r;
    END;
    $$ LANGUAGE plpgsql;''',

    # --- TRIGGERS ---

    '''DROP TRIGGER IF EXISTS tr_audit_profesores ON profesores;
    CREATE TRIGGER tr_audit_profesores
    AFTER INSERT OR UPDATE OR DELETE ON profesores
    FOR EACH ROW EXECUTE FUNCTION fn_audit_profesores();''',

    '''DROP TRIGGER IF EXISTS tr_audit_alumnos ON alumnos;
    CREATE TRIGGER tr_audit_alumnos
    AFTER INSERT OR UPDATE OR DELETE ON alumnos
    FOR EACH ROW EXECUTE FUNCTION fn_audit_alumnos();''',

    '''DROP TRIGGER IF EXISTS tr_audit_cursos ON cursos;
    CREATE TRIGGER tr_audit_cursos
    AFTER INSERT OR UPDATE OR DELETE ON cursos
    FOR EACH ROW EXECUTE FUNCTION fn_audit_cursos();''',

    # --- ÍNDICES ---

    '''CREATE INDEX IF NOT EXISTS idx_alumnos_nombre ON alumnos (nombre);''',
    '''CREATE INDEX IF NOT EXISTS idx_alumnos_apellido ON alumnos (apellido);''',
    '''CREATE INDEX IF NOT EXISTS idx_alumnos_dinero ON alumnos (dinero);''',
    '''CREATE INDEX IF NOT EXISTS idx_profesores_nombre ON profesores (nombre);''',
    '''CREATE INDEX IF NOT EXISTS idx_profesores_apellido ON profesores (apellido);''',
    
    # Índice GIN para búsqueda rápida en JSONB
    '''CREATE INDEX IF NOT EXISTS idx_cursos_nombres_jsonb ON cursos USING GIN (nombres_multi);''',
    
    '''CREATE INDEX IF NOT EXISTS idx_cursos_precio ON cursos (precio);''',
    '''CREATE INDEX IF NOT EXISTS idx_cursos_capacidad ON cursos (capacidad_max);''',
    '''CREATE INDEX IF NOT EXISTS idx_matriculas_alumno ON matriculas (id_alumno);''',
    '''CREATE INDEX IF NOT EXISTS idx_matriculas_curso ON matriculas (id_curso);'''
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