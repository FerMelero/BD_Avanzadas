"""Rutas del recurso parts (listado y dibujo binario)."""
from __future__ import annotations

from flask import Blueprint, Response, abort, render_template, request, redirect, url_for

from models.db import get_cursos, estadisticas_cursos_filter, get_cursos_by_id, get_alumnos_by_curso, crear_curso, get_profesores, modificar_curso, delete_curso, view_audit_cursos, search_cursos, dinero_recaudado_curso_y_profesor, capacidad_total_rollup


cursos_bp = Blueprint("cursos", __name__, url_prefix="/cursos")


@cursos_bp.route("")
def list_():
    """Lista de cursos con búsqueda opcional."""
    # 1. Captura de parámetros
    nombre = request.args.get("nombre", None)
    id_profesor = request.args.get("id_profesor", None)
    id_curso = request.args.get("id_curso", None)
    precio_min = request.args.get("precio_min", None)
    precio_max = request.args.get("precio_max", None)
    capacidad_min = request.args.get("capacidad_min", None)
    page = request.args.get("page", 1, type=int)
    limit = request.args.get("limit", 10, type=int)
    offset = (page - 1) * limit
    
    # 2. Normalización de strings y conversión manual (sin funciones extra)
    if nombre is not None:
        nombre = nombre.strip() or None
        
    if id_profesor and id_profesor.strip():
        try:
            id_profesor = int(id_profesor)
        except ValueError:
            id_profesor = None
    else:
        id_profesor = None
    
    if id_curso and id_curso.strip():
        try:
            id_curso = int(id_curso)
        except ValueError:
            id_curso = None
    else:
        id_curso = None
    
    if precio_min and precio_min.strip():
        try:
            precio_min = float(precio_min)
        except ValueError:
            precio_min = None
    else:
        precio_min = None
    
    if precio_max and precio_max.strip():
        try:
            precio_max = float(precio_max)
        except ValueError:
            precio_max = None
    else:
        precio_max = None
    
    if capacidad_min and capacidad_min.strip():
        try:
            capacidad_min = int(capacidad_min)
        except ValueError:
            capacidad_min = None
    else:
        capacidad_min = None
    
    # 3. Lógica de búsqueda
    # Verificamos si hay algún parámetro para filtrar
    if nombre or id_profesor is not None or id_curso is not None or precio_min is not None or precio_max is not None or capacidad_min is not None:
        cursos = search_cursos(
            nombre=nombre,
            id_profesor=id_profesor,
            id_curso=id_curso,
            precio_min=precio_min,
            precio_max=precio_max,
            capacidad_min=capacidad_min,
            offset=offset,
            limit=limit
        )
        search_active = True
    else:
        cursos = search_cursos(offset=offset, limit=limit)
        search_active = False
    
    # 4. Renderizado
    return render_template(
        "cursos.html",
        cursos=cursos,
        search_active=search_active,
        page=page,
        limit=limit,
        nombre=nombre,
        id_profesor=id_profesor,
        id_curso=id_curso,
        precio_min=precio_min,
        precio_max=precio_max,
        capacidad_min=capacidad_min
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

@cursos_bp.route("/nuevo", methods=["GET", "POST"])
def new_curso():
    profesores = get_profesores()
    print(profesores)
    if request.method == "POST":
        nombres = {
        "es" : request.form["nombre_es"],
        "en" : request.form["nombre_en"]}
        id_profesor = request.form["id_profesor"]
        capacidad_max = int(request.form["capacidad_max"])
        precio = float(request.form["precio"])
            
        if precio < 0:
            return "Error: El precio no puede ser negativo", 400 
        curso_id = crear_curso(nombres, id_profesor, capacidad_max, precio)

        if curso_id: 
            return redirect(url_for("cursos.view_curso", id_curso=curso_id))
        else:
            return "Error al crear el curso en la base de datos", 500
    
    return render_template("crearCurso.html", profesores=profesores)

@cursos_bp.route("/modificar/<int:id_curso>", methods=["GET", "POST"])
def edit_curso(id_curso):
    if request.method == "POST":
        nombres = {"es" : request.form["nombre_curso_es"],
        "en" : request.form["nombre_curso_en"]}
        id_prof = request.form["id_profesor"]
        precio = float(request.form["precio"])
        capacidad = int(request.form["capacidad_max"])

        if modificar_curso(id_curso, nombres, id_prof, precio, capacidad):
            return redirect(url_for("cursos.view_curso", id_curso = id_curso))
        else:
            return "Error al actualizar curso", 500

    curso_obj = get_cursos_by_id(id_curso)
    profs = get_profesores()
    
    if not curso_obj:
        return "Curso no encontrado", 404
        
    return render_template("modificarCurso.html", curso=curso_obj, profesores=profs)

@cursos_bp.route("/eliminar/<int:id_curso>", methods=["GET", "POST"])
def eliminar_curso(id_curso):
    curso = get_cursos_by_id(id_curso)
    if request.method == "POST":
        eliminacion = delete_curso(id_curso)
        if eliminacion:
            return redirect (url_for("cursos.list_",))
    
    if not curso:
        return "Curso no encontrado", 404
        
    return render_template("eliminarCurso.html", curso=curso)

@cursos_bp.route("/auditoria")
def auditoria_cursos():
    aud_cursos = view_audit_cursos()
    return render_template("audCursos.html", aud = aud_cursos)

@cursos_bp.route("/dinero")
def dinero():
    resultado = dinero_recaudado_curso_y_profesor()
    return render_template("dineroRecaud.html", result = resultado)

@cursos_bp.route("/reporte-capacidades")
def reporte_capacidades():
    resultado = capacidad_total_rollup()
    return render_template("reporteRollup.html", result=resultado)

@cursos_bp.route("/estadisticas-precios")
def estadisticas_precios():
    resultado = estadisticas_cursos_filter()
    return render_template("reporteFilter.html", result=resultado)