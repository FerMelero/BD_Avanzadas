from __future__ import annotations

from flask import Blueprint, Response, abort, render_template, request, redirect, url_for

from models.db import get_profesores, get_profesor_by_id, get_cursos_by_profesor, view_audit_profesores, crear_profesor, modificar_profesor, delete_profesor, search_profesores


profesores_bp = Blueprint("profesores", __name__, url_prefix="/profesores")


@profesores_bp.route("")
def list_():
    """Lista de profesores con búsqueda opcional."""
    nombre = request.args.get("nombre", None)
    apellido = request.args.get("apellido", None)
    dni = request.args.get("dni", None)
    fecha_nacimiento = request.args.get("fecha_nacimiento", None)
    page = request.args.get("page", 1, type=int)
    limit = request.args.get("limit", 10, type=int)
    offset = (page - 1) * limit
    
    # Si hay parámetros de búsqueda, usar búsqueda filtrada
    if nombre or apellido or dni or fecha_nacimiento:
        profesores = search_profesores(
            nombre=nombre,
            apellido=apellido,
            dni=dni,
            fecha_nacimiento=fecha_nacimiento,
            offset=offset,
            limit=limit
        )
        search_active = True
    else:
        profesores = search_profesores(offset=offset, limit=limit)
        search_active = False
    
    return render_template(
        "profesores.html",
        profesores=profesores,
        search_active=search_active,
        page=page,
        limit=limit,
        nombre=nombre,
        apellido=apellido,
        dni=dni,
        fecha_nacimiento=fecha_nacimiento
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

@profesores_bp.route("/modificar/<int:id_profesor>", methods=["GET", "POST"])
def edit_profesor(id_profesor):
    profesor = get_profesor_by_id(id_profesor)
    if request.method == "POST":
        nombre = request.form["nombre"]
        apellido = request.form["apellido"]
        fecha_nacimiento = request.form["fecha_nacimiento"]
        dni = request.form["dni"]

        mod_profesor = modificar_profesor(id_profesor, nombre, apellido, fecha_nacimiento, dni)

        if mod_profesor:
            return redirect(url_for("profesores.view_profesor", id_profesor=id_profesor))
        else:
            return "Error al mdoficiar el profesor en la base de datos", 500
    
    return render_template("modificarProfesor.html", profesor = profesor)

@profesores_bp.route("/eliminar/<int:id_profesor>", methods=["GET", "POST"])
def eliminar_profesor(id_profesor):
    profesor = get_profesor_by_id(id_profesor)
    if request.method == "POST":
        eliminacion = delete_profesor(id_profesor)
        if eliminacion:
            return redirect (url_for("profesores.list_",))
    
    if not profesor:
        return "Profesor no encontrado", 404
        
    return render_template("eliminarProfesor.html", profesor=profesor)
