from __future__ import annotations

import psycopg

from config import load_config


def insert_profesor(nombre: str, apellido: str, fecha_nacimiento: str, dni: str) -> int:
    """Insert a vendor and return vendor_id."""
    sql = "INSERT INTO profesores(nombre, apellido, fecha_nacimiento, dni) VALUES (%s, %s, %s, %s);"
    cfg = load_config()
    with psycopg.connect(**cfg) as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (nombre, apellido, fecha_nacimiento, dni))
    return True

def insert_alumno(nombre: str, apellido: str, fecha_nacimiento: str, dni: str) -> int:
    """Insert a vendor and return vendor_id."""
    sql = "INSERT INTO alumnos(nombre, apellido, fecha_nacimiento, dni) VALUES (%s, %s, %s, %s);"
    cfg = load_config()
    with psycopg.connect(**cfg) as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (nombre, apellido, fecha_nacimiento, dni))
    return True

def insert_cursos(nombre_curso: str, id_profesor: int) -> int:
    """Insert a vendor and return vendor_id."""
    sql = "INSERT INTO cursos(nombre_curso, id_profesor) VALUES (%s, %s);"
    cfg = load_config()
    with psycopg.connect(**cfg) as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (nombre_curso, id_profesor))
    return True

def insert_matriculas(id_alumno: int, id_profesor: int) -> int:
    """Insert a vendor and return vendor_id."""
    sql = "INSERT INTO matriculas(nombre_curso, id_profesor) VALUES (%s, %s);"
    cfg = load_config()
    with psycopg.connect(**cfg) as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (id_alumno, id_profesor))
    return True



if __name__ == "__main__":
    v_id = insert_vendor("ACME Corporation")
    p_id = insert_part("Speaker")
    assign_part_to_vendor(v_id, p_id)
    print(f"Inserted vendor_id={v_id}, part_id={p_id} and assigned relation.")
