"""Rutas del recurso parts (listado y dibujo binario)."""
from __future__ import annotations

from flask import Blueprint, Response, abort, render_template

from models.db import get_alumnos, get_alumno_by_id, get_cursos_by_alumno


alumnos_bp = Blueprint("alumnos", __name__, url_prefix="/alumnos")


@alumnos_bp.route("")
def list_():
    """Lista de alumnos."""
    alumnos = get_alumnos()
    return render_template(
        "alumnos.html",
        alumnos=alumnos
    )

@alumnos_bp.route("/<int:id_alumno>") # le pasamos un ID
def view_alumno(id_alumno):
    print("ID recibido:", id_alumno) # depuración
    alumno = get_alumno_by_id(id_alumno) # pasar un ID a la función y pasarlo para render
    curso = get_cursos_by_alumno(id_alumno)
    return render_template(
        "idAlumno.html",
        alumno=alumno,
        cursos = curso
    )

