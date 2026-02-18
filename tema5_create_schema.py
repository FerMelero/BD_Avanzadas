from __future__ import annotations

import argparse

import psycopg

from config import load_config


DDL = [
    # Profesores
    """
    CREATE TABLE IF NOT EXISTS profesores (
        profesor_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        nombre TEXT NOT NULL
    );
    """,
    # Alumnos
    """
    CREATE TABLE IF NOT EXISTS alumnos (
        alumno_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        nombre TEXT NOT NULL,
        email TEXT NOT NULL
    );
    """,
    # Cursos
    """
    CREATE TABLE IF NOT EXISTS cursos (
        curso_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        profesor_id BIGINT NOT NULL REFERENCES profesores(profesor_id),
        titulo TEXT NOT NULL
    );
    """,
    # Matrículas (N:M)
    """
    CREATE TABLE IF NOT EXISTS matriculas (
        matricula_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        alumno_id BIGINT NOT NULL REFERENCES alumnos(alumno_id),
        curso_id BIGINT NOT NULL REFERENCES cursos(curso_id)
    );
    """,
]

DROP = [
    "DROP TABLE IF EXISTS matriculas;",
    "DROP TABLE IF EXISTS cursos;",
    "DROP TABLE IF EXISTS alumnos;",
    "DROP TABLE IF EXISTS profesores;",
]


def create_schema(drop: bool) -> None:
    cfg = load_config()
    with psycopg.connect(**cfg) as conn:
        with conn.cursor() as cur:
            if drop:
                for stmt in DROP:
                    cur.execute(stmt)
            for stmt in DDL:
                cur.execute(stmt)
        conn.commit()
    print("OK: esquema Tema 5 creado." + (" (drop previo)" if drop else ""))


def main() -> None:
    parser = argparse.ArgumentParser(description="Crea el esquema del Tema 5 (alumnos/profesores/cursos/matriculas).")
    parser.add_argument("--drop", action="store_true", help="Borra tablas antes de crear.")
    args = parser.parse_args()
    create_schema(drop=args.drop)


if __name__ == "__main__":
    main()
