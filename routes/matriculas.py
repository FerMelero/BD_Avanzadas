"""Rutas del recurso parts (listado y dibujo binario)."""
from __future__ import annotations

from flask import Blueprint, Response, abort, render_template, request, redirect, url_for

from models.db import get_matriculas, crear_matricula, demo_transaccion_rollback, get_alumnos, get_cursos


matriculas_bp = Blueprint("matriculas", __name__, url_prefix="/matriculas")


@matriculas_bp.route("")
def list_():
    """Lista de parts. Incluye indicador de cuáles tienen dibujo."""
    matriculas = get_matriculas()
    return render_template(
        "matriculas.html",
        matriculas=matriculas
    )

@matriculas_bp.route("/nuevo", methods=["GET", "POST"])
def matricular_alumno():
    alumnos = get_alumnos()
    cursos = get_cursos()
    error=None
    if request.method == "POST":
        id_alumno = request.form["id_alumno"]
        id_curso = request.form["id_curso"]
        resultado = crear_matricula(id_alumno, id_curso)

        if resultado == True:
            return redirect(url_for("matriculas.list_"))
        else:
            error = resultado
    return render_template("matricularAlumno.html", error=error, alumnos=alumnos, cursos=cursos)

@matriculas_bp.route("/demo-rollback")
def demo_rollback():
    demo_transaccion_rollback()
    return "Rollback ejecutado"

    