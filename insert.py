from __future__ import annotations

import psycopg
import random

from config import load_config
from faker import Faker

fake = Faker("es_ES")

'''
==================
Inserción de datos
==================
'''

def insert_profesor(nombre: str, apellido: str, fecha_nacimiento: str, dni: str) -> int:
    sql = "INSERT INTO profesores(nombre, apellido, fecha_nacimiento, dni) VALUES (%s, %s, %s, %s) RETURNING id_profesor;"
    cfg = load_config()
    with psycopg.connect(**cfg) as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (nombre, apellido, fecha_nacimiento, dni))
            return cur.fetchone()[0] # nos sirve para devolver el ID

def insert_alumno(nombre: str, apellido: str, fecha_nacimiento: str, dni: str) -> int:
    sql = "INSERT INTO alumnos(nombre, apellido, fecha_nacimiento, dni) VALUES (%s, %s, %s, %s) RETURNING id_alumno;"
    cfg = load_config()
    with psycopg.connect(**cfg) as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (nombre, apellido, fecha_nacimiento, dni))
            return cur.fetchone()[0] # nos sirve para devolver el ID

def insert_cursos(nombre_curso: str, id_profesor: int) -> int:
    sql = "INSERT INTO cursos(nombre_curso, id_profesor) VALUES (%s, %s) RETURNING id_curso;"
    cfg = load_config()
    with psycopg.connect(**cfg) as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (nombre_curso, id_profesor))
            return cur.fetchone()[0] # nos sirve para devolver el ID

def insert_matriculas(id_curso: int, id_alumno: int) -> int:
    sql = "INSERT INTO matriculas(id_curso, id_alumno) VALUES (%s, %s);"
    cfg = load_config()
    with psycopg.connect(**cfg) as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (id_curso, id_alumno))
    return True

'''
===================
Genearción de datos
===================
'''

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

def fake_curso(profesores_ids):
    return {
        "nombre_curso": fake.word(),
        "id_profesor": random.choice(profesores_ids)
    }

'''
======================================
Funciones finales de inserción de datos
======================================
'''

def final_insert_alumnos(val):
    print("Insertando ALUMNOS")
    alumnos_IDS=[]
    for _ in range(val): 
        alumno = fake_alumno() 
        alumno_id = insert_alumno( alumno["nombre"], alumno["apellido"], alumno["fecha_nacimiento"], alumno["dni"] ) # con esta inserción devuelve el ID gracias a la función anterior
        alumnos_IDS.append(alumno_id)
    print("Listo.")
    return alumnos_IDS

def final_insert_profesores(val):
    print("Insertando PROFESORES")
    profesores_ids=[]
    for _ in range(val): 
        profesor = fake_profesor() 
        profesor_id = insert_profesor( profesor["nombre"], profesor["apellido"], profesor["fecha_nacimiento"], profesor["dni"] ) 
        profesores_ids.append(profesor_id)
    print("Listo.")
    return profesores_ids

def final_insert_cursos(val, profesores_ids):
    print("Insertando CURSOS")
    cursos_ids = []

    for _ in range(val):
        curso = fake_curso(profesores_ids)
        curso_id = insert_cursos(
            curso["nombre_curso"],
            curso["id_profesor"]
        )
        cursos_ids.append(curso_id)

    print("Cursos insertados.")
    return cursos_ids

def final_insert_matriculas(cursos_ids, alumnos_ids, alumnos_por_curso=5):
    print("Insertando MATRICULAS")

    for curso_id in cursos_ids:
        alumnos_curso = random.sample(alumnos_ids, min(alumnos_por_curso, len(alumnos_ids)))

        for alumno_id in alumnos_curso:
            insert_matriculas(curso_id, alumno_id)

    print("Matrículas insertadas.")

'''
====
Main
====
'''

if __name__ == "__main__":
    profesores_ids = final_insert_profesores(10)  # guardamos IDs
    alumnos_ids = final_insert_alumnos(20)        # guardamos IDs
    cursos_ids = final_insert_cursos(10, profesores_ids)

    final_insert_matriculas(cursos_ids, alumnos_ids, alumnos_por_curso=5)

