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