from __future__ import annotations

import psycopg

from config import load_config

from models.entities import Alumno, Profesor, Matriculas, Cursos

#from models.entities import Part, Vendor

def get_connection():
    cfg = load_config()
    return psycopg.connect(**cfg)

def get_alumnos():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id_alumno, nombre, apellido, fecha_nacimiento, DNI FROM alumnos ORDER BY id_alumno;"
            )
            return [Alumno(id=r[0], name=r[1]) for r in cur.fetchall()]

def get_profesores():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id_profesor, nombre, apellido, fecha_nacimiento, DNI FROM profesores ORDER BY id_profesor;"
            )
            return [Alumno(id=r[0], name=r[1]) for r in cur.fetchall()]

def get_cursos():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id_curso, nombre_curso, id_profesor FROM cursos ORDER BY id_curso;"
            )
            return [Alumno(id=r[0], name=r[1]) for r in cur.fetchall()]

def get_matriculas():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id_alumno, id_curso FROM matriculas ORDER BY id_alumno;"
            )
            return [Alumno(id=r[0], name=r[1]) for r in cur.fetchall()]
