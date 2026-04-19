from __future__ import annotations

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
class Cursos:
    id_curso: int
    nombre_curso: str
    id_profesor: int
    precio: float
    capacidad_max: int

@dataclass(frozen=True)
class Matriculas:
    id_alumno: int
    id_curso: int

@dataclass(frozen=True)
class AuditCurso:
    operacion: str
    stamp: date
    user_id: str
    nombre_curso: str
    id_curso: int
    precio_curso: float

@dataclass(frozen=True)
class AuditProfesor:
    operacion: str
    stamp: date
    user_id: str
    nombre: str
    id_profesor: int
    dni: str

@dataclass(frozen=True)
class AuditAlumno:
    operacion: str
    stamp: date
    user_id: str
    nombre: str
    id_alumno: int
    dni: str

@dataclass(frozen=True)
class AuditCurso:
    operacion: str
    stamp: date
    user_id: str
    nombre_curso: str
    id_curso: int
    precio_curso: str