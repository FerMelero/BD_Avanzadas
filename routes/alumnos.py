"""Rutas del recurso parts (listado y dibujo binario)."""
from __future__ import annotations

from flask import Blueprint, Response, abort, render_template

from models.db import get_alumnos


alumnos_bp = Blueprint("alumnos", __name__, url_prefix="/alumnos")


@alumnos_bp.route("")
def list_():
    """Lista de parts. Incluye indicador de cuáles tienen dibujo."""
    alumnos = get_alumnos()
    return render_template(
        "alumnos.html",
        alumnos=alumnos
    )

