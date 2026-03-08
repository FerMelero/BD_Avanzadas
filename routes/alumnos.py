"""Rutas del recurso parts (listado y dibujo binario)."""
from __future__ import annotations

from flask import Blueprint, Response, abort, render_template, request, redirect, url_for

from models.db import get_alumnos, get_alumno_by_id, get_cursos_by_alumno, crear_alumno


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

@alumnos_bp.route("/nuevo", methods=["GET", "POST"])
def new_alumno():
    if request.method == "POST":
        nombre = request.form["nombre_alumno"]
        apellidos = request.form["apellidos_alumno"]
        fecha_nacimiento_alumno = request.form["fecha_nacimiento_alumno"]
        dni = request.form["dni_alumno"]
        nuevo_alumno = crear_alumno(nombre, apellidos, fecha_nacimiento_alumno, dni)
        return redirect(url_for("alumnos.view_alumno", id_alumno=nuevo_alumno))
    
    return render_template("crearAlumno.html")