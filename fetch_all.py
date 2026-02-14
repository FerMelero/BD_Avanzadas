from __future__ import annotations

import psycopg

from config import load_config


def get_vendors() -> list[tuple]:
    cfg = load_config()
    with psycopg.connect(**cfg) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT vendor_id, vendor_name FROM vendors ORDER BY vendor_id;")
            return cur.fetchall()


if __name__ == "__main__":
    for row in get_vendors():
        print(row)
