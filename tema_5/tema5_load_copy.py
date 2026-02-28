from __future__ import annotations

import argparse
from pathlib import Path

import psycopg

from config import load_config


def _copy_from_csv(cur: psycopg.Cursor, table: str, columns: list[str], csv_path: Path) -> None:
    cols = ", ".join(columns)
    sql = f"COPY {table} ({cols}) FROM STDIN WITH (FORMAT csv, HEADER true)"
    with csv_path.open("r", encoding="utf-8") as f:
        with cur.copy(sql) as copy:
            for line in f:
                copy.write(line)


def load_all(data_dir: Path) -> None:
    cfg = load_config()
    profesores_csv = data_dir / "profesores.csv"
    alumnos_csv = data_dir / "alumnos.csv"
    cursos_csv = data_dir / "cursos.csv"
    matriculas_csv = data_dir / "matriculas.csv"

    missing = [p for p in [profesores_csv, alumnos_csv, cursos_csv, matriculas_csv] if not p.exists()]
    if missing:
        raise SystemExit(f"Faltan CSV: {', '.join(str(p) for p in missing)}. Ejecuta tema5_generate_csv.py primero.")

    with psycopg.connect(**cfg) as conn:
        with conn.cursor() as cur:
            # Importante: respetar orden por FKs
            print("COPY profesores...")
            _copy_from_csv(cur, "profesores", ["profesor_id", "nombre"], profesores_csv)

            print("COPY alumnos...")
            _copy_from_csv(cur, "alumnos", ["alumno_id", "nombre", "email"], alumnos_csv)

            print("COPY cursos...")
            _copy_from_csv(cur, "cursos", ["curso_id", "profesor_id", "titulo"], cursos_csv)

            print("COPY matriculas...")
            _copy_from_csv(cur, "matriculas", ["alumno_id", "curso_id"], matriculas_csv)

        conn.commit()

    print("OK: carga masiva completada con COPY.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Carga CSV del Tema 5 con COPY (modo serio).")
    parser.add_argument("--data-dir", default="data_tema5", help="Directorio con CSV (default: data_tema5).")
    args = parser.parse_args()
    load_all(Path(args.data_dir))


if __name__ == "__main__":
    main()
