from __future__ import annotations

import psycopg

from config import load_config

from models.entities import Alumno, Profesor, Matriculas, Cursos

def get_connection():
    cfg = load_config()
    return psycopg.connect(**cfg)

def get_alumnos():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id_alumno, nombre, apellido, fecha_nacimiento, dni FROM alumnos ORDER BY id_alumno;"
            )
            return [Alumno(*r) for r in cur.fetchall()]

def get_profesores():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id_profesor, nombre, apellido, fecha_nacimiento, DNI FROM profesores ORDER BY id_profesor;"
            )
            return [Profesor(*r) for r in cur.fetchall()]

def get_cursos():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id_curso, nombre_curso, id_profesor FROM cursos ORDER BY id_curso;"
            )
            return [Cursos(*r) for r in cur.fetchall()]

def get_matriculas():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id_alumno, id_curso FROM matriculas ORDER BY id_alumno;"
            )
            return [Matriculas(*r) for r in cur.fetchall()]

def get_alumno_by_id(id_alumno): # pasamos un ID específico
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
            "SELECT id_alumno, nombre, apellido, fecha_nacimiento, dni FROM alumnos WHERE id_alumno=%s;",
            (id_alumno,) # debemos poner %s(id_alumno, ) para que seleccione bien el ID
        )
            row = cur.fetchone()
            print("Fila obtenida:", row) # depuración
            if row:
                return Alumno(*row) # ahora solo se devuelve un objeto que es una fila
            return None
