"""Rutas del recurso parts (listado y dibujo binario)."""
from __future__ import annotations

from flask import Blueprint, Response, abort, render_template

from models.db import get_profesores


profesores_bp = Blueprint("profesores", __name__, url_prefix="/profesores")


@profesores_bp.route("")
def list_():
    """Lista de parts. Incluye indicador de cuáles tienen dibujo."""
    profesores = get_profesores()
    return render_template(
        "profesores.html",
        profesores=profesores
    )

