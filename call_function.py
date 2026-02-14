from __future__ import annotations

import psycopg

from config import load_config


def get_parts_by_vendor(vendor_id: int) -> list[tuple[int, str]]:
    """Call SQL function get_parts_by_vendor(id) and return rows."""
    cfg = load_config()
    with psycopg.connect(**cfg) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT part_id, part_name FROM get_parts_by_vendor(%s);", (vendor_id,))
            return cur.fetchall()


if __name__ == "__main__":
    rows = get_parts_by_vendor(1)
    for r in rows:
        print(r)
