from __future__ import annotations

import psycopg

from config import load_config


def iter_rows(batch_size: int = 10):
    cfg = load_config()
    with psycopg.connect(**cfg) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT vendor_id, vendor_name FROM vendors ORDER BY vendor_id;")
            while True:
                rows = cur.fetchmany(batch_size)
                if not rows:
                    break
                for row in rows:
                    yield row


if __name__ == "__main__":
    for r in iter_rows(batch_size=2):
        print(r)
