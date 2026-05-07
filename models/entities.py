from __future__ import annotations

import json

from dataclasses import dataclass
from datetime import date

@dataclass(frozen=True)
class Alumno:
    id_alumno: int
    nombre: str
    apellido: str
    fecha_nacimiento: date
    dni: str
    dinero: float


@dataclass(frozen=True)
class Profesor:
    id_profesor: int
    nombre: str
    apellido: str
    fecha_nacimiento: date
    dni: str

@dataclass(frozen=True)
class Asignaturas:
    id_asignatura: int
    nombre_asignatura: str
    id_profesor: int
    precio: float
    capacidad_max: int

@dataclass(frozen=True)
class Matriculas:
    id_alumno: int
    id_asignatura: int

@dataclass(frozen=True)
class Auditasignatura:
    operacion: str
    stamp: date
    user_id: str
    nombre_asignatura: str
    id_asignatura: int
    precio_asignatura: float

@dataclass(frozen=True)
class AuditProfesor:
    operacion: str
    stamp: date
    user_id: str
    id_profesor: int
    nombre: str
    apellido: str
    fecha_nacimiento: date
    dni: str

@dataclass(frozen=True)
class AuditAlumno:
    operacion: str
    stamp: date
    user_id: str
    id_alumno: int
    nombre: str
    apellido: str
    fecha_nacimiento: date
    dni: str
    dinero: float

@dataclass(frozen=True)
class Auditasignatura:
    operacion: str
    stamp: date
    user_id: str
    id_asignatura: int
    nombres_multi: json
    id_profesor: int
    capacidad_max: int
    precio: float