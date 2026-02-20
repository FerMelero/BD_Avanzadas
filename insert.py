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
# los parámetros del servidor no se tocan para obtener mejores consultas sino más rápido
def fake_curso(profesores_id):
    return {
        "nombre_curso": fake.word(),
        "id_alumno": random.choice(range(1,10)) # este range se modifica en función de los alumnos que hay para no isnertar elementos no existentes
    } # TO DO: terminar el archivo

def fake_matricula():
    return

def final_insert_alumnos(val):
    print("Insertando ALUMNOS")
    for _ in range(val): 
        alumno = fake_alumno() 
        insert_profesor( alumno["nombre"], alumno["apellido"], alumno["fecha_nacimiento"], alumno["dni"] ) 
    print("Listo.")

def final_insert_profesores(val):
    print("Insertando PROFESORES")
    for _ in range(val): 
        profesor = fake_profesor() 
        insert_profesor( profesor["nombre"], profesor["apellido"], profesor["fecha_nacimiento"], profesor["dni"] ) 
    print("Listo.")

if __name__ == "__main__":
    final_insert_alumnos(10)
    final_insert_profesores(10)

