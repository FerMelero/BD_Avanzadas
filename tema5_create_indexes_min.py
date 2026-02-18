from __future__ import annotations

import psycopg

from config import load_config


DDL = [
    # Patrón: por profesor -> cursos
    "CREATE INDEX IF NOT EXISTS idx_cursos_profesor_id ON cursos(profesor_id);",
    # Patrón: por alumno -> matriculas
    "CREATE INDEX IF NOT EXISTS idx_matriculas_alumno_id ON matriculas(alumno_id);",
    # Patrón: por curso -> matriculas
    "CREATE INDEX IF NOT EXISTS idx_matriculas_curso_id ON matriculas(curso_id);",
]


def main() -> None:
    cfg = load_config()
    with psycopg.connect(**cfg) as conn:
        with conn.cursor() as cur:
            for stmt in DDL:
                cur.execute(stmt)
        conn.commit()
    print("OK: índices mínimos creados.")
    print("Siguiente paso: python tema5_explain_queries.py --profesor-id 1 --alumno-id 1")


if __name__ == "__main__":
    main()
