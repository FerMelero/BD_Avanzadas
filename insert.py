from __future__ import annotations

import psycopg
import random

from config import load_config
from faker import Faker

fake = Faker("es_ES")


def insert_profesor(nombre: str, apellido: str, fecha_nacimiento: str, dni: str) -> int:
    sql = "INSERT INTO profesores(nombre, apellido, fecha_nacimiento, dni) VALUES (%s, %s, %s, %s);"
    cfg = load_config()
    with psycopg.connect(**cfg) as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (nombre, apellido, fecha_nacimiento, dni))
    return True

def insert_alumno(nombre: str, apellido: str, fecha_nacimiento: str, dni: str) -> int:
    sql = "INSERT INTO alumnos(nombre, apellido, fecha_nacimiento, dni) VALUES (%s, %s, %s, %s);"
    cfg = load_config()
    with psycopg.connect(**cfg) as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (nombre, apellido, fecha_nacimiento, dni))
    return True

def insert_cursos(nombre_curso: str, id_profesor: int) -> int:
    sql = "INSERT INTO cursos(nombre_curso, id_profesor) VALUES (%s, %s);"
    cfg = load_config()
    with psycopg.connect(**cfg) as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (nombre_curso, id_profesor))
    return True

def insert_matriculas(id_alumno: int, id_profesor: int) -> int:
    sql = "INSERT INTO matriculas(nombre_curso, id_profesor) VALUES (%s, %s);"
    cfg = load_config()
    with psycopg.connect(**cfg) as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (id_alumno, id_profesor))
    return True

def fake_profesor():
    return {
        "nombre": fake.first_name(),
        "apellido": fake.last_name(),
        "fecha_nacimiento": fake.date_between(start_date='-55y', end_date='-23y'),
        "dni": fake.nif()
    }

def fake_alumno():
    return {
        "nombre": fake.first_name(),
        "apellido": fake.last_name(),
        "fecha_nacimiento": fake.date_between(start_date='-30y', end_date='-15y'),
        "dni": fake.nif()
    }

def fake_curso(profesores_id):
    materias = [
        "Programación",
        "Bases de Datos",
        "Redes",
        "Sistemas Operativos",
        "Inteligencia Artificial"
    ]
        
    return {
        "nombre_curso": f"{random.choice(materias)}",
        "id_profesor": random.choice(profesores_id)
    }

def fake_matricula():
    return


if __name__ == "__main__":
    print(f"Inserted vendor_id={v_id}, part_id={p_id} and assigned relation.")
