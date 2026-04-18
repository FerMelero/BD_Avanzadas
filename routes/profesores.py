from __future__ import annotations

from flask import Blueprint, Response, abort, render_template, request, redirect, url_for

from models.db import get_profesores, get_profesor_by_id, get_cursos_by_profesor,view_audit_profesores, crear_profesor


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

@profesores_bp.route("/auditoria")
def auditoria_profesores():
    aud_profesores = view_audit_profesores()
    return render_template("audProfesores.html", aud = aud_profesores)

@profesores_bp.route("/nuevo", methods=["GET", "POST"])
def new_profesor():
    if request.method == "POST":
        nombre = request.form["nombre_profesor"]
        apellido = request.form["apellido_profesor"]
        fecha_nac = request.form["fecha_nacimiento"] 
        dni = request.form["dni_profesor"]

        id_nuevo = crear_profesor(nombre, apellido, fecha_nac, dni)

        if id_nuevo:
            return redirect(url_for("profesores.view_profesor", id_profesor = id_nuevo))
        else:
            return "Error al crear el profesor", 500

    return render_template("crearProfesor.html")
