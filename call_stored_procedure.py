from __future__ import annotations

import psycopg

from config import load_config


def add_new_part(part_name: str, vendor_name: str) -> None:
    """Call stored procedure add_new_part(new_part_name, new_vendor_name)."""
    cfg = load_config()
    with psycopg.connect(**cfg) as conn:
        with conn.cursor() as cur:
            cur.execute("CALL add_new_part(%s, %s);", (part_name, vendor_name))


if __name__ == "__main__":
    add_new_part("New Part (proc)", "New Vendor (proc)")
    print("Procedure executed.")
