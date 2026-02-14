from __future__ import annotations

import psycopg

from config import load_config


def delete_part(part_id: int) -> int:
    """Delete a part by id; returns number of deleted rows."""
    sql = "DELETE FROM parts WHERE part_id = %s;"
    cfg = load_config()
    with psycopg.connect(**cfg) as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (part_id,))
            return cur.rowcount


if __name__ == "__main__":
    n = delete_part(1)
    print(f"Rows deleted: {n}")
