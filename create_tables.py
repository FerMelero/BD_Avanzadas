from __future__ import annotations

import psycopg

from config import load_config




DDL = ('CREATE TABLE IF NOT EXISTS vendors (\n    vendor_id SERIAL PRIMARY KEY,\n    vendor_name VARCHAR(255) NOT NULL\n);', 'CREATE TABLE IF NOT EXISTS parts (\n    part_id SERIAL PRIMARY KEY,\n    part_name VARCHAR(255) NOT NULL\n);', 'CREATE TABLE IF NOT EXISTS part_drawings (\n    part_id INTEGER PRIMARY KEY,\n    file_extension VARCHAR(5) NOT NULL,\n    drawing_data BYTEA NOT NULL,\n    FOREIGN KEY (part_id)\n        REFERENCES parts (part_id)\n        ON UPDATE CASCADE\n        ON DELETE CASCADE\n);', 'CREATE TABLE IF NOT EXISTS vendor_parts (\n    vendor_id INTEGER NOT NULL,\n    part_id INTEGER NOT NULL,\n    PRIMARY KEY (vendor_id, part_id),\n    FOREIGN KEY (vendor_id)\n        REFERENCES vendors (vendor_id)\n        ON UPDATE CASCADE\n        ON DELETE CASCADE,\n    FOREIGN KEY (part_id)\n        REFERENCES parts (part_id)\n        ON UPDATE CASCADE\n        ON DELETE CASCADE\n);')


def create_tables() -> None:
    """Create demo tables for the lab (idempotent)."""
    cfg = load_config()
    with psycopg.connect(**cfg) as conn:
        with conn.cursor() as cur:
            for stmt in DDL:
                cur.execute(stmt)
    print("Tables created (or already existed).")


if __name__ == "__main__":
    create_tables()
