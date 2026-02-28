from __future__ import annotations

import psycopg

from config import load_config


SQL_TABLES = """
SELECT
    relname AS tabla,
    n_live_tup AS filas_vivas,
    n_dead_tup AS filas_muertas,
    seq_scan,
    idx_scan
FROM pg_stat_user_tables
WHERE relname IN ('profesores','alumnos','cursos','matriculas')
ORDER BY relname;
"""

SQL_INDEXES = """
SELECT
    relname AS tabla,
    indexrelname AS indice,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch
FROM pg_stat_user_indexes
WHERE relname IN ('profesores','alumnos','cursos','matriculas')
ORDER BY relname, indexrelname;
"""


def _print_table(cur, title: str, sql: str) -> None:
    cur.execute(sql)
    rows = cur.fetchall()
    cols = [d.name for d in cur.description]

    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)
    print(" | ".join(cols))
    print("-" * 80)
    for r in rows:
        print(" | ".join(str(x) for x in r))


def main() -> None:
    cfg = load_config()
    with psycopg.connect(**cfg) as conn:
        with conn.cursor() as cur:
            _print_table(cur, "pg_stat_user_tables (uso de seq scan vs idx scan)", SQL_TABLES)
            _print_table(cur, "pg_stat_user_indexes (uso por índice)", SQL_INDEXES)


if __name__ == "__main__":
    main()
