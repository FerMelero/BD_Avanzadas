from __future__ import annotations

import argparse
import textwrap

import psycopg

from config import load_config


SQL_BY_PROFESOR = """
SELECT
    c.profesor_id,
    COUNT(DISTINCT m.alumno_id) AS alumnos_distintos
FROM cursos c
JOIN matriculas m ON m.curso_id = c.curso_id
WHERE c.profesor_id = %s
GROUP BY c.profesor_id;
"""

SQL_BY_ALUMNO = """
SELECT
    m.alumno_id,
    COUNT(DISTINCT c.profesor_id) AS profesores_distintos
FROM matriculas m
JOIN cursos c ON c.curso_id = m.curso_id
WHERE m.alumno_id = %s
GROUP BY m.alumno_id;
"""


def explain(cur: psycopg.Cursor, sql: str, params: tuple) -> None:
    stmt = "EXPLAIN (ANALYZE, BUFFERS, VERBOSE) " + sql
    cur.execute(stmt, params)
    rows = cur.fetchall()
    print("\n".join(r[0] for r in rows))


def main() -> None:
    parser = argparse.ArgumentParser(description="Ejecuta EXPLAIN (ANALYZE, BUFFERS, VERBOSE) para las consultas objetivo.")
    parser.add_argument("--profesor-id", type=int, default=1, help="ID de profesor para la consulta por profesor.")
    parser.add_argument("--alumno-id", type=int, default=1, help="ID de alumno para la consulta por alumno.")
    args = parser.parse_args()

    cfg = load_config()
    with psycopg.connect(**cfg) as conn:
        with conn.cursor() as cur:
            print("=" * 80)
            print("CONSULTA 1 (por profesor) — objetivo: cursos del profesor y alumnos distintos")
            print("=" * 80)
            print(textwrap.dedent(SQL_BY_PROFESOR).strip())
            print("-" * 80)
            explain(cur, SQL_BY_PROFESOR, (args.profesor_id,))

            print("\n" + "=" * 80)
            print("CONSULTA 2 (por alumno) — objetivo: cursos del alumno y profesores distintos")
            print("=" * 80)
            print(textwrap.dedent(SQL_BY_ALUMNO).strip())
            print("-" * 80)
            explain(cur, SQL_BY_ALUMNO, (args.alumno_id,))


if __name__ == "__main__":
    main()
