from __future__ import annotations

import psycopg

from config import load_config


def analyze() -> None:
    cfg = load_config()
    with psycopg.connect(**cfg) as conn:
        with conn.cursor() as cur:
            # ANALYZE global: en laboratorio sirve para dejar estadísticas consistentes
            cur.execute("ANALYZE;")
        conn.commit()
    print("OK: ANALYZE ejecutado (estadísticas actualizadas).")


if __name__ == "__main__":
    analyze()
