from __future__ import annotations

import psycopg

from config import load_config


def insert_vendor(vendor_name: str) -> int:
    """Insert a vendor and return vendor_id."""
    sql = "INSERT INTO vendors(vendor_name) VALUES (%s) RETURNING vendor_id;"
    cfg = load_config()
    with psycopg.connect(**cfg) as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (vendor_name,))
            vendor_id = cur.fetchone()[0]
    return int(vendor_id)


def insert_part(part_name: str) -> int:
    """Insert a part and return part_id."""
    sql = "INSERT INTO parts(part_name) VALUES (%s) RETURNING part_id;"
    cfg = load_config()
    with psycopg.connect(**cfg) as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (part_name,))
            part_id = cur.fetchone()[0]
    return int(part_id)


def assign_part_to_vendor(vendor_id: int, part_id: int) -> None:
    sql = "INSERT INTO vendor_parts(vendor_id, part_id) VALUES (%s, %s);"
    cfg = load_config()
    with psycopg.connect(**cfg) as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (vendor_id, part_id))


if __name__ == "__main__":
    v_id = insert_vendor("ACME Corporation")
    p_id = insert_part("Speaker")
    assign_part_to_vendor(v_id, p_id)
    print(f"Inserted vendor_id={v_id}, part_id={p_id} and assigned relation.")
