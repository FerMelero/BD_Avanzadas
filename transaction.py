from __future__ import annotations

import psycopg
from psycopg import errors

from config import load_config


def add_part_atomic(part_name: str, vendor_id: int) -> int:
    """Single atomic operation: insert ONE part and assign it to ONE vendor.

    If vendor_id does not exist, the whole operation fails and nothing is inserted.
    """
    sql_part = "INSERT INTO parts(part_name) VALUES (%s) RETURNING part_id;"
    sql_rel = "INSERT INTO vendor_parts(vendor_id, part_id) VALUES (%s, %s);"

    cfg = load_config()
    with psycopg.connect(**cfg) as conn:
        with conn.cursor() as cur:
            cur.execute(sql_part, (part_name,))
            part_id = cur.fetchone()[0]
            cur.execute(sql_rel, (vendor_id, part_id))
    return int(part_id)


def add_part_transactional(part_name: str, vendor_ids: list[int]) -> int:
    """Transactional flow: insert a part and assign it to multiple vendors.

    This is a multi-step business flow. If any step fails (e.g., a vendor id does not exist),
    the transaction is rolled back and the part is NOT inserted.
    """
    sql_part = "INSERT INTO parts(part_name) VALUES (%s) RETURNING part_id;"
    sql_rel = "INSERT INTO vendor_parts(vendor_id, part_id) VALUES (%s, %s);"

    cfg = load_config()
    with psycopg.connect(**cfg) as conn:
        try:
            with conn.cursor() as cur:
                cur.execute(sql_part, (part_name,))
                part_id = cur.fetchone()[0]
                for v_id in vendor_ids:
                    cur.execute(sql_rel, (v_id, part_id))
            # If we reach here, context manager commits automatically.
            return int(part_id)
        except errors.ForeignKeyViolation as exc:
            # Raising triggers rollback by the connection context manager.
            print("Foreign key violation -> ROLLBACK:", exc)
            raise


if __name__ == "__main__":
    # Example 1: atomic operation (should succeed if vendor_id=1 exists)
    try:
        p1 = add_part_atomic("Power Amplifier (atomic)", 1)
        print("Inserted part (atomic):", p1)
    except Exception as exc:
        print("Atomic insert failed:", exc)

    # Example 2: transactional flow (force a failure with a non-existing vendor id)
    try:
        p2 = add_part_transactional("Power Amplifier (tx)", [1, 999999])
        print("Inserted part (tx):", p2)
    except Exception:
        print("Transactional flow failed as expected. Check that no partial data was inserted.")
