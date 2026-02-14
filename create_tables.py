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
        dni VARCHAR(20) NOT NULL UNIQUE
    );''',

    # Cursos (1 profesor por curso)
    '''CREATE TABLE IF NOT EXISTS cursos (
        id_curso SERIAL PRIMARY KEY,
        nombre_curso VARCHAR(100) NOT NULL,
        id_profesor INTEGER NOT NULL,
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
    );'''
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
