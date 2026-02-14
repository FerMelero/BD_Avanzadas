from __future__ import annotations

import psycopg

from config import load_config


def update_vendor(vendor_id: int, vendor_name: str) -> int:
    """Update vendor name; returns number of affected rows."""
    sql = "UPDATE vendors SET vendor_name = %s WHERE vendor_id = %s;"
    cfg = load_config()
    with psycopg.connect(**cfg) as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (vendor_name, vendor_id))
            return cur.rowcount


if __name__ == "__main__":
    n = update_vendor(1, "ACME Corporation (updated)")
    print(f"Rows updated: {n}")
