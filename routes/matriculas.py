"""Rutas del recurso parts (listado y dibujo binario)."""
from __future__ import annotations

from flask import Blueprint, Response, abort, render_template

from models.db import get_matriculas


matriculas_bp = Blueprint("matriculas", __name__, url_prefix="/matriculas")


@matriculas_bp.route("")
def list_():
    """Lista de parts. Incluye indicador de cuáles tienen dibujo."""
    matriculas = get_matriculas()
    return render_template(
        "matriculas.html",
        matriculas=matriculas
    )

