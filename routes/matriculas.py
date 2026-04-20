"""Rutas del recurso parts (listado y dibujo binario)."""
from __future__ import annotations

from flask import Blueprint, Response, abort, render_template, request, redirect, url_for

from models.db import get_matriculas, get_matriculas_vista, crear_matricula, demo_transaccion_rollback, get_alumnos, get_cursos, search_matriculas, search_matriculas_vista


matriculas_bp = Blueprint("matriculas", __name__, url_prefix="/matriculas")


@matriculas_bp.route("")
def list_():
    """Lista de matriculas con búsqueda opcional."""
    id_curso = request.args.get("id_curso", None, type=int)
    id_alumno = request.args.get("id_alumno", None, type=int)
    page = request.args.get("page", 1, type=int)
    limit = request.args.get("limit", 10, type=int)
    offset = (page - 1) * limit
    
    # Si hay parámetros de búsqueda, usar búsqueda filtrada
    if id_curso or id_alumno:
        matriculas = search_matriculas(
            id_curso=id_curso,
            id_alumno=id_alumno,
            offset=offset,
            limit=limit
        )
        search_active = True
    else:
        matriculas = search_matriculas(offset=offset, limit=limit)
        search_active = False
    
    return render_template(
        "matriculas.html",
        matriculas=matriculas,
        search_active=search_active,
        page=page,
        limit=limit,
        id_curso=id_curso,
        id_alumno=id_alumno
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

@matriculas_bp.route("/vista")
def vista_matriculas():
    """Vista de alumnos-profesores-cursos con búsqueda opcional."""
    nombre_alumno = request.args.get("nombre_alumno", None)
    nombre_profesor = request.args.get("nombre_profesor", None)
    nombre_curso = request.args.get("nombre_curso", None)
    page = request.args.get("page", 1, type=int)
    limit = request.args.get("limit", 10, type=int)
    offset = (page - 1) * limit
    
    # Si hay parámetros de búsqueda, usar búsqueda filtrada
    if nombre_alumno or nombre_profesor or nombre_curso:
        vista = search_matriculas_vista(
            nombre_alumno=nombre_alumno,
            nombre_profesor=nombre_profesor,
            nombre_curso=nombre_curso,
            offset=offset,
            limit=limit
        )
        search_active = True
    else:
        vista = search_matriculas_vista(offset=offset, limit=limit)
        search_active = False
    
    return render_template(
        "vistaMatriculas.html",
        vista=vista,
        search_active=search_active,
        page=page,
        limit=limit,
        nombre_alumno=nombre_alumno,
        nombre_profesor=nombre_profesor,
        nombre_curso=nombre_curso
    )

@matriculas_bp.route("/demo-rollback")
def demo_rollback():
    demo_transaccion_rollback()
    return "Rollback ejecutado"

    