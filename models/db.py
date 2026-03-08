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


def get_cursos_by_alumno(id_alumno):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT c.id_curso, c.nombre_curso, c.id_profesor
                FROM cursos c
                JOIN matriculas m ON c.id_curso = m.id_curso
                WHERE m.id_alumno = %s;
                """,
                (id_alumno,)
            )

            rows = cur.fetchall()
            print("Cursos obtenidos:", rows)

            return [Cursos(*r) for r in rows]


def get_profesor_by_id(id_profesor): # pasamos un ID específico
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
            "SELECT p.id_profesor, p.nombre, p.apellido, p.fecha_nacimiento, p.dni FROM profesores p WHERE p.id_profesor=%s;",
            (id_profesor,) # debemos poner %s(id_profesor, ) para que seleccione bien el ID
        )
            row = cur.fetchone()
            print("Fila obtenida:", row) # depuración
            if row:
                return Profesor(*row) # ahora solo se devuelve un objeto que es una fila
            return None

def get_cursos_by_profesor(id_profesor): # pasamos un ID específico
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
            "SELECT id_curso, nombre_curso, id_profesor FROM cursos WHERE id_profesor=%s;",
            (id_profesor,) # debemos poner %s(id_profesor, ) para que seleccione bien el ID
        )
            rows = cur.fetchall()
            print("Fila obtenida:", rows) # depuración
            return [Cursos(*r) for r in rows]

def get_cursos_by_id(id_curso):
    with get_connection() as conn:
        with conn.cursor() as cur:
            print("Buscando curso con id:", id_curso)
            cur.execute(
            "SELECT id_curso, nombre_curso, id_profesor FROM cursos WHERE id_curso=%s;",
            (id_curso,) # debemos poner %s(id_curso, ) para que seleccione bien el ID
        )
            row = cur.fetchone()
            print("Fila obtenida:", row) # depuración
            if row:
                return Cursos(*row) # ahora solo se devuelve un objeto que es una fila
            return None

def get_alumnos_by_curso(id_curso):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
            "SELECT a.id_alumno, a.nombre, a.apellido, a.fecha_nacimiento, a.dni FROM alumnos a JOIN matriculas m ON a.id_alumno = m.id_alumno WHERE m.id_curso=%s;",
            (id_curso,) # debemos poner %s(id_curso, ) para que seleccione bien el ID
        )
            rows = cur.fetchall()
            print("Fila obtenida:", rows) # depuración
            return [Alumno(*r) for r in rows]

def crear_alumno(nombre, apellidos, fecha_nacimiento_alumno, dni):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO alumnos (nombre, apellido, fecha_nacimiento, dni) VALUES (%s, %s, %s, %s) RETURNING id_alumno;",
                (nombre, apellidos, fecha_nacimiento_alumno, dni)
            )
            id_alumno = cur.fetchone()[0]
    return id_alumno