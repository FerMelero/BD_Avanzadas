from __future__ import annotations

import psycopg

from config import load_config


DDL = [
    # Índice compuesto (elige el orden según navegación dominante)
    # Aquí elegimos (asignatura_id, alumno_id) porque la consulta por profesor entra por asignaturas y luego baja a matriculas por asignatura.
    "CREATE INDEX IF NOT EXISTS idx_matriculas_asignatura_alumno ON matriculas(asignatura_id, alumno_id);",
    # Unicidad (si el modelo lo exige): evita duplicados y además crea un índice útil.
    # OJO: si tu dataset genera duplicados, este UNIQUE fallará.
    # Actívalo solo si primero generas matriculas sin duplicados, o si limpias staging.
    # "ALTER TABLE matriculas ADD CONSTRAINT uq_matriculas_alumno_asignatura UNIQUE (alumno_id, asignatura_id);"
]


def main() -> None:
    cfg = load_config()
    with psycopg.connect(**cfg) as conn:
        with conn.cursor() as cur:
            for stmt in DDL:
                cur.execute(stmt)
        conn.commit()
    print("OK: índices finos creados (compuestos).")
    print("Siguiente paso: python tema5_explain_queries.py --profesor-id 1 --alumno-id 1")


if __name__ == "__main__":
    main()
