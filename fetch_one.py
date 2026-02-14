from __future__ import annotations

import psycopg

from config import load_config


def get_vendor(vendor_id: int) -> tuple | None:
    cfg = load_config()
    with psycopg.connect(**cfg) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT vendor_id, vendor_name FROM vendors WHERE vendor_id = %s;",
                (vendor_id,),
            )
            return cur.fetchone()


if __name__ == "__main__":
    print(get_vendor(1))
