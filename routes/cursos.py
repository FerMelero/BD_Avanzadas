"""Rutas del recurso parts (listado y dibujo binario)."""
from __future__ import annotations

from flask import Blueprint, Response, abort, render_template, request, redirect, url_for

from models.db import get_cursos, get_cursos_by_id, get_alumnos_by_curso, crear_curso, get_profesores


cursos_bp = Blueprint("cursos", __name__, url_prefix="/cursos")


@cursos_bp.route("")
def list_():
    """Lista de parts. Incluye indicador de cuáles tienen dibujo."""
    cursos = get_cursos()
    return render_template(
        "cursos.html",
        cursos=cursos
    )

@cursos_bp.route("/<int:id_curso>")
def view_curso(id_curso):
    print("ID recibido:", id_curso)

    curso = get_cursos_by_id(id_curso)
    alumnos = get_alumnos_by_curso(id_curso)

    return render_template(
        "idCurso.html",
        curso=curso,
        alumnos=alumnos
    )

@cursos_bp.route("/nuevo", methods=["GET", "POST"])
def new_curso():
    profesores = get_profesores()
    if request.method == "POST":
        nombre_curso = request.form["nombre_curso"]
        id_profesor = request.form["id_profesor"]
        capacidad_max = int(request.form["capacidad_max"])
        precio = float(request.form["precio"])
            
        if precio < 0:
            return "Error: El precio no puede ser negativo", 400 
        curso_id = crear_curso(nombre_curso, id_profesor, capacidad_max, precio)

        if curso_id: 
            return redirect(url_for("cursos.view_curso", id_curso=curso_id))
        else:
            return "Error al crear el curso en la base de datos", 500
    
    return render_template("crearCurso.html", profesores=profesores)
