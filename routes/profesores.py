from __future__ import annotations

from flask import Blueprint, Response, abort, render_template

from models.db import get_profesores, get_profesor_by_id, get_cursos_by_profesor


profesores_bp = Blueprint("profesores", __name__, url_prefix="/profesores")


@profesores_bp.route("")
def list_():
    """Lista de profesores."""
    profesores = get_profesores()
    return render_template(
        "profesores.html",
        profesores=profesores
    )

@profesores_bp.route("/<int:id_profesor>") # le pasamos un ID
def view_profesor(id_profesor):
    print("ID recibido:", id_profesor) # depuración
    profesor = get_profesor_by_id(id_profesor) # pasar un ID a la función y pasarlo para render
    cursos = get_cursos_by_profesor(id_profesor)
    return render_template(
        "idProfesor.html",
        profesor=profesor,
        cursos=cursos
        
    )
