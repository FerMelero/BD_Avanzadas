"""Rutas del recurso parts (listado y dibujo binario)."""
from __future__ import annotations

from flask import Blueprint, Response, abort, render_template

from models.db import get_cursos


cursos_bp = Blueprint("cursos", __name__, url_prefix="/cursos")


@cursos_bp.route("")
def list_():
    """Lista de parts. Incluye indicador de cuáles tienen dibujo."""
    cursos = get_cursos()
    return render_template(
        "cursos.html",
        cursos=cursos
    )

