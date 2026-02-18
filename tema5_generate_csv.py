from __future__ import annotations

import argparse
import csv
import os
import random
from pathlib import Path


def _safe_email(i: int) -> str:
    # email determinista, sin Faker (más rápido)
    return f"alumno{i}@example.edu"


def generate_csv(
    out_dir: Path,
    profesores: int,
    alumnos: int,
    cursos: int,
    matriculas: int,
    seed: int,
) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    rnd = random.Random(seed)

    profesores_csv = out_dir / "profesores.csv"
    alumnos_csv = out_dir / "alumnos.csv"
    cursos_csv = out_dir / "cursos.csv"
    matriculas_csv = out_dir / "matriculas.csv"

    # Profesores (ids 1..profesores)
    with profesores_csv.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["profesor_id", "nombre"])
        for pid in range(1, profesores + 1):
            w.writerow([pid, f"Profesor {pid}"])

    # Alumnos (ids 1..alumnos)
    with alumnos_csv.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["alumno_id", "nombre", "email"])
        for aid in range(1, alumnos + 1):
            w.writerow([aid, f"Alumno {aid}", _safe_email(aid)])

    # Cursos (ids 1..cursos), cada curso asignado a un profesor aleatorio
    with cursos_csv.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["curso_id", "profesor_id", "titulo"])
        for cid in range(1, cursos + 1):
            pid = rnd.randint(1, profesores)
            w.writerow([cid, pid, f"Curso {cid}"])

    # Matrículas: (alumno_id, curso_id)
    # Generación rápida con random. Ojo: puede generar duplicados; para el laboratorio vale.
    with matriculas_csv.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["alumno_id", "curso_id"])
        for _ in range(matriculas):
            aid = rnd.randint(1, alumnos)
            cid = rnd.randint(1, cursos)
            w.writerow([aid, cid])

    print("OK: CSV generados en:", out_dir)
    print(" -", profesores_csv.name)
    print(" -", alumnos_csv.name)
    print(" -", cursos_csv.name)
    print(" -", matriculas_csv.name)
    print()
    print("Siguiente paso: python tema5_load_copy.py --data-dir", out_dir)


def main() -> None:
    parser = argparse.ArgumentParser(description="Genera CSV sintético para Tema 5 (listo para COPY).")
    parser.add_argument("--data-dir", default="data_tema5", help="Directorio de salida (default: data_tema5).")
    parser.add_argument("--profesores", type=int, default=100, help="Número de profesores.")
    parser.add_argument("--alumnos", type=int, default=10_000, help="Número de alumnos.")
    parser.add_argument("--cursos", type=int, default=5_000, help="Número de cursos.")
    parser.add_argument("--matriculas", type=int, default=50_000, help="Número de matrículas.")
    parser.add_argument("--seed", type=int, default=42, help="Semilla para reproducibilidad.")
    args = parser.parse_args()

    generate_csv(
        out_dir=Path(args.data_dir),
        profesores=args.profesores,
        alumnos=args.alumnos,
        cursos=args.cursos,
        matriculas=args.matriculas,
        seed=args.seed,
    )


if __name__ == "__main__":
    main()
