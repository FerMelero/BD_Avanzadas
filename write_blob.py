from __future__ import annotations

from pathlib import Path

import psycopg

from config import load_config


def write_blob(part_id: int, path_to_file: str) -> None:
    """Store a file as BYTEA in part_drawings."""
    cfg = load_config()
    data = Path(path_to_file).read_bytes()
    ext = Path(path_to_file).suffix.lstrip(".")[:5] or "bin"

    sql = """
    INSERT INTO part_drawings(part_id, file_extension, drawing_data)
    VALUES (%s, %s, %s)
    ON CONFLICT (part_id) DO UPDATE
      SET file_extension = EXCLUDED.file_extension,
          drawing_data   = EXCLUDED.drawing_data;
    """

    with psycopg.connect(**cfg) as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (part_id, ext, data))


if __name__ == "__main__":
    # Requires an existing part_id (create one via insert.py)
    write_blob(1, "images/input/speaker.png")
    print("BLOB written.")
