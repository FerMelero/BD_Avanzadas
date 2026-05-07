from __future__ import annotations

import psycopg

from config import load_config


DDL = [
    # Patrón: por profesor -> asignaturas
    "CREATE INDEX IF NOT EXISTS idx_asignaturas_profesor_id ON asignaturas(profesor_id);",
    # Patrón: por alumno -> matriculas
    "CREATE INDEX IF NOT EXISTS idx_matriculas_alumno_id ON matriculas(alumno_id);",
    # Patrón: por asignatura -> matriculas
    "CREATE INDEX IF NOT EXISTS idx_matriculas_asignatura_id ON matriculas(asignatura_id);",
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
