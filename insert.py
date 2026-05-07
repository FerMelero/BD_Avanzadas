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

# insertamos profesor y devolvemos los ids para su futuro uso
def insert_profesor(nombre: str, apellido: str, fecha_nacimiento: str, dni: str) -> int:
    sql = "INSERT INTO profesores(nombre, apellido, fecha_nacimiento, dni) VALUES (%s, %s, %s, %s) RETURNING id_profesor;"
    cfg = load_config()
    with psycopg.connect(**cfg) as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (nombre, apellido, fecha_nacimiento, dni))
            return cur.fetchone()[0] # nos sirve para devolver el ID

# insertamos alumno y devolvemos los ids para su futuro uso
def insert_alumno(nombre: str, apellido: str, fecha_nacimiento: str, dni: str, dinero: float) -> int:
    sql = "INSERT INTO alumnos(nombre, apellido, fecha_nacimiento, dni, dinero) VALUES (%s, %s, %s, %s, %s) RETURNING id_alumno;"
    cfg = load_config()
    with psycopg.connect(**cfg) as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (nombre, apellido, fecha_nacimiento, dni, dinero))
            return cur.fetchone()[0] # nos sirve para devolver el ID

# insertamos asignatura y devolvemos los ids para su futuro uso
def insert_asignaturas(nombre_asignatura: str, id_profesor: int, capacidad_max: int, precio: float) -> int:
    sql = "INSERT INTO asignaturas(nombre_asignatura, id_profesor, capacidad_max, precio) VALUES (%s, %s, %s, %s) RETURNING id_asignatura;"
    cfg = load_config()
    with psycopg.connect(**cfg) as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (nombre_asignatura, id_profesor, capacidad_max, precio))
            return cur.fetchone()[0] # nos sirve para devolver el ID

# no hace falta devolver id porque es la relación entre 2 tablas
def insert_matriculas(id_asignatura: int, id_alumno: int) -> int:
    sql = "INSERT INTO matriculas(id_asignatura, id_alumno) VALUES (%s, %s);"
    cfg = load_config()
    with psycopg.connect(**cfg) as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (id_asignatura, id_alumno))
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
        "dni": fake.nif(),
        "dinero": round(random.uniform(100, 2000), 2)
    }
# los parámetros del servidor no se tocan para obtener mejores consultas sino más rápido

def fake_asignatura(profesores_ids):
    return {
        "nombre_asignatura": fake.word(),
        "id_profesor": random.choice(profesores_ids),
        "capacidad_max": random.randint(15, 40),
        "precio": round(random.uniform(50, 400), 2)
    }
# no añadimos fake_matricula porque es la relación entre 2 tablas

'''
======================================
Funciones finales de inserción de datos
======================================
'''

def final_insert_alumnos(val):
    print("Insertando ALUMNOS")
    alumnos_IDS=[] # almacenar IDS temporalmente
    for _ in range(val): 
        alumno = fake_alumno() 
        alumno_id = insert_alumno( alumno["nombre"], alumno["apellido"], alumno["fecha_nacimiento"], alumno["dni"], alumno["dinero"] ) # con esta inserción devuelve el ID gracias a la función anterior
        alumnos_IDS.append(alumno_id)
    print("Listo.")
    return alumnos_IDS

def final_insert_profesores(val):
    print("Insertando PROFESORES")
    profesores_ids=[] # almacenar IDS temporalmente
    for _ in range(val): 
        profesor = fake_profesor() 
        profesor_id = insert_profesor( profesor["nombre"], profesor["apellido"], profesor["fecha_nacimiento"], profesor["dni"] ) 
        profesores_ids.append(profesor_id)
    print("Listo.")
    return profesores_ids

def final_insert_asignaturas(val, profesores_ids):
    print("Insertando ASIGNATURAS")
    asignaturas_ids = [] # almacenar IDS temporalmente

    for _ in range(val):
        asignatura = fake_asignatura(profesores_ids)
        asignatura_id = insert_asignaturas(
            asignatura["nombre_asignatura"],
            asignatura["id_profesor"],
            asignatura["capacidad_max"],
            asignatura["precio"]
        )
        asignaturas_ids.append(asignatura_id)

    print("Listo.")
    return asignaturas_ids

def final_insert_matriculas(asignaturas_ids, alumnos_ids, alumnos_por_asignatura=5):
    print("Insertando MATRICULAS")

    for asignatura_id in asignaturas_ids:
        alumnos_asignatura = random.sample(alumnos_ids, min(alumnos_por_asignatura, len(alumnos_ids))) # controlar la inserción

        for alumno_id in alumnos_asignatura:
            insert_matriculas(asignatura_id, alumno_id)

    print("Matrículas insertadas.")

'''
====
Main
====
'''

if __name__ == "__main__":
    final_insert_profesores(50)
    final_insert_alumnos(1000)
