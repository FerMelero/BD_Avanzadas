from __future__ import annotations

from pathlib import Path

import psycopg

from config import load_config


def read_blob(part_id: int, output_dir: str = "images/output") -> Path:
    """Read BYTEA from part_drawings and write it back to disk."""
    cfg = load_config()
    sql = "SELECT file_extension, drawing_data FROM part_drawings WHERE part_id = %s;"

    with psycopg.connect(**cfg) as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (part_id,))
            row = cur.fetchone()
            if not row:
                raise RuntimeError(f"No drawing found for part_id={part_id}")
            ext, data = row

    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    out_path = out / f"part_{part_id}.{ext}"
    out_path.write_bytes(data)
    return out_path


if __name__ == "__main__":
    p = read_blob(1)
    print("BLOB restored to:", p)
