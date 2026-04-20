"""Rutas del recurso parts (listado y dibujo binario)."""
from __future__ import annotations

from flask import Blueprint, Response, abort, render_template, request, redirect, url_for

from models.db import get_alumnos, get_alumno_by_id, get_cursos_by_alumno, crear_alumno, view_audit_alumnos, modificar_alumno, delete_alumno, search_alumnos


alumnos_bp = Blueprint("alumnos", __name__, url_prefix="/alumnos")


@alumnos_bp.route("")
def list_():
    """Lista de alumnos con búsqueda opcional."""
    # Obtener parámetros de búsqueda de la query string
    nombre = request.args.get("nombre", None)
    apellido = request.args.get("apellido", None)
    dni = request.args.get("dni", None)
    dinero_min = request.args.get("dinero_min", None)
    dinero_max = request.args.get("dinero_max", None)
    page = request.args.get("page", 1, type=int)
    limit = request.args.get("limit", 10, type=int)
    offset = (page - 1) * limit
    
    # Normalizar strings vacíos a None
    if nombre is not None:
        nombre = nombre.strip() or None
    if apellido is not None:
        apellido = apellido.strip() or None
    if dni is not None:
        dni = dni.strip() or None
    
    # Convertir dinero a float si está presente
    if dinero_min and dinero_min.strip():
        try:
            dinero_min = float(dinero_min)
        except ValueError:
            dinero_min = None
    else:
        dinero_min = None
    
    if dinero_max and dinero_max.strip():
        try:
            dinero_max = float(dinero_max)
        except ValueError:
            dinero_max = None
    else:
        dinero_max = None
    
    # Si hay parámetros de búsqueda, usar búsqueda filtrada
    if nombre or apellido or dni or dinero_min or dinero_max:
        alumnos = search_alumnos(
            nombre=nombre,
            apellido=apellido,
            dni=dni,
            dinero_min=dinero_min,
            dinero_max=dinero_max,
            offset=offset,
            limit=limit
        )
        search_active = True
    else:
        # Si no hay búsqueda, devolver todos con paginación
        alumnos = search_alumnos(offset=offset, limit=limit)
        search_active = False
    
    return render_template(
        "alumnos.html",
        alumnos=alumnos,
        search_active=search_active,
        page=page,
        limit=limit,
        nombre=nombre,
        apellido=apellido,
        dni=dni,
        dinero_min=dinero_min,
        dinero_max=dinero_max
    )

@alumnos_bp.route("/<int:id_alumno>") # le pasamos un ID
def view_alumno(id_alumno):
    print("ID recibido:", id_alumno) # depuración
    alumno = get_alumno_by_id(id_alumno) # pasar un ID a la función y pasarlo para render
    curso = get_cursos_by_alumno(id_alumno)
    return render_template(
        "idAlumno.html",
        alumno=alumno,
        cursos = curso
    )

@alumnos_bp.route("/nuevo", methods=["GET", "POST"])
def new_alumno():
    if request.method == "POST":
        nombre = request.form["nombre_alumno"]
        apellidos = request.form["apellidos_alumno"]
        fecha_nacimiento_alumno = request.form["fecha_nacimiento_alumno"]
        dni = request.form["dni_alumno"]
        dinero = float(request.form["dinero_alumno"])
        if dinero < 0:
            return "Error: El dinero no puede ser negativo", 400 
            
        nuevo_alumno = crear_alumno(nombre, apellidos, fecha_nacimiento_alumno, dni, dinero)

        if nuevo_alumno:
            return redirect(url_for("alumnos.view_alumno", id_alumno=nuevo_alumno))
        else:
            return "Error al crear el alumno en la base de datos", 500
    
    return render_template("crearAlumno.html")

@alumnos_bp.route("/auditoria")
def auditoria_alumnos():
    aud_alumnos = view_audit_alumnos()
    print(len(aud_alumnos))
    return render_template("audAlumnos.html", aud = aud_alumnos)

@alumnos_bp.route("/modificar/<int:id_alumno>", methods=["GET", "POST"])
def edit_alumno(id_alumno):
    alumno = get_alumno_by_id(id_alumno)
    if request.method == "POST":
        nombre = request.form["nombre"]
        apellido = request.form["apellido"]
        fecha_nacimiento = request.form["fecha_nacimiento"]
        dni = request.form["dni"]
        dinero = float(request.form["dinero"])
        if dinero < 0:
            return "Error: El dinero no puede ser negativo", 400 
            
        mod_alumno = modificar_alumno(id_alumno, nombre, apellido, fecha_nacimiento, dni, dinero)

        if mod_alumno:
            return redirect(url_for("alumnos.view_alumno", id_alumno=id_alumno))
        else:
            return "Error al crear el alumno en la base de datos", 500
    
    return render_template("modificarAlumno.html", alumno = alumno)

@alumnos_bp.route("/eliminar/<int:id_alumno>", methods=["GET", "POST"])
def eliminar_alumno(id_alumno):
    alumno = get_alumno_by_id(id_alumno)
    if request.method == "POST":
        eliminacion = delete_alumno(id_alumno)
        if eliminacion:
            return redirect (url_for("alumnos.list_",))
    
    if not alumno:
        return "Alumno no encontrado", 404
        
    return render_template("eliminarAlumno.html", alumno=alumno)

