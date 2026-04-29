from __future__ import annotations
import psycopg
from config import load_config
DDL = (
    # 1. LIMPIEZA TOTAL (Elimina tablas y vistas previas para evitar conflictos)
    '''DROP VIEW IF EXISTS vista_alumnos_profesores_cursos CASCADE;''',
    '''DROP TABLE IF EXISTS matriculas CASCADE;''',
    '''DROP TABLE IF EXISTS cursos CASCADE;''',
    '''DROP TABLE IF EXISTS alumnos CASCADE;''',
    '''DROP TABLE IF EXISTS profesores CASCADE;''',
    '''DROP TABLE IF EXISTS audit_profesores CASCADE;''',
    '''DROP TABLE IF EXISTS audit_alumnos CASCADE;''',
    '''DROP TABLE IF EXISTS audit_cursos CASCADE;''',

    # 2. EXTENSIONES DEL TEMA 12
    # Forzamos el esquema public para evitar errores de "función no encontrada"
    '''CREATE EXTENSION IF NOT EXISTS pg_trgm SCHEMA public;''',
    '''CREATE EXTENSION IF NOT EXISTS unaccent SCHEMA public;''',

    # 3. FUNCIÓN DE SOPORTE PARA ÍNDICES (TEMA 12)
    # Necesaria para indexar unaccent, ya que por defecto no es IMMUTABLE
    '''CREATE OR REPLACE FUNCTION unaccent_immutable(text)
    RETURNS text AS $$
        SELECT public.unaccent($1);
    $$ LANGUAGE sql IMMUTABLE PARALLEL SAFE;''',

    # 4. TABLAS DE LA APLICACIÓN
    
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

    # Tabla Cursos (Multi-idioma con JSONB - Requisito Tema 12)
    '''CREATE TABLE cursos (
        id_curso SERIAL PRIMARY KEY,
        nombres_multi JSONB NOT NULL,
        id_profesor INTEGER NOT NULL REFERENCES profesores(id_profesor) ON DELETE CASCADE,
        capacidad_max INTEGER NOT NULL,
        precio FLOAT NOT NULL
    );''',

    # Tabla Matrículas (Relación N:M)
    '''CREATE TABLE matriculas (
        id_alumno INTEGER NOT NULL REFERENCES alumnos(id_alumno) ON DELETE CASCADE,
        id_curso INTEGER NOT NULL REFERENCES cursos(id_curso) ON DELETE CASCADE,
        PRIMARY KEY (id_alumno, id_curso)
    );''',

    # 5. AUDITORÍA (Triggers y Tablas)
    '''CREATE TABLE audit_cursos(
        operacion CHAR(1), stamp TIMESTAMP, user_id VARCHAR(100), 
        id_curso INTEGER, nombres_multi JSONB, id_profesor INTEGER, 
        capacidad_max INTEGER, precio FLOAT
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

    # 6. VISTA (Extracción de datos del JSONB)
    '''CREATE VIEW vista_alumnos_profesores_cursos AS
    SELECT a.nombre || ' ' || a.apellido AS nombre_alumno,
           p.nombre || ' ' || p.apellido AS nombre_profesor,
           c.nombres_multi->>'es' AS nombre_curso
    FROM matriculas m
    JOIN alumnos a ON m.id_alumno = a.id_alumno
    JOIN cursos c ON m.id_curso = c.id_curso
    JOIN profesores p ON c.id_profesor = p.id_profesor;''',

    # 7. ÍNDICES AVANZADOS (TEMA 12 - RENDIMIENTO)
    
    # Índice GIN para búsquedas por clave/valor dentro del JSONB
    '''CREATE INDEX idx_cursos_nombres_jsonb ON cursos USING GIN (nombres_multi);''',
    
    # Índices GIST para Fuzzy Search e ignorar acentos simultáneamente
    '''CREATE INDEX idx_cursos_fuzzy_es ON cursos 
       USING gist (unaccent_immutable(nombres_multi->>'es') gist_trgm_ops);''',
    
    '''CREATE INDEX idx_cursos_fuzzy_en ON cursos 
       USING gist (unaccent_immutable(nombres_multi->>'en') gist_trgm_ops);''',

    # Otros índices de búsqueda rápida
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