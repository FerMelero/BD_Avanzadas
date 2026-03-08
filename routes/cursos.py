"""Rutas del recurso parts (listado y dibujo binario)."""
from __future__ import annotations

from flask import Blueprint, Response, abort, render_template

from models.db import get_cursos, get_cursos_by_id, get_alumnos_by_curso


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
