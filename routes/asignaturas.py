"""Rutas del recurso parts (listado y dibujo binario)."""
from __future__ import annotations

from flask import Blueprint, Response, abort, render_template, request, redirect, url_for

from models.db import (
    get_asignaturas,
    estadisticas_asignaturas_filter,
    get_asignaturas_by_id,
    get_asignatura_area,
    get_alumnos_by_asignatura,
    crear_asignatura,
    get_profesores,
    modificar_asignatura,
    delete_asignatura,
    view_audit_asignaturas,
    search_asignaturas,
    dinero_recaudado_asignatura_y_profesor,
    capacidad_total_rollup,
    upsert_asignatura_poligono,
)


asignaturas_bp = Blueprint("asignaturas", __name__, url_prefix="/asignaturas")


@asignaturas_bp.route("")
def list_():
    """Lista de asignaturas con búsqueda opcional."""
    # 1. Captura de parámetros
    nombre = request.args.get("nombre", None)
    id_profesor = request.args.get("id_profesor", None)
    id_asignatura = request.args.get("id_asignatura", None)
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
    
    if id_asignatura and id_asignatura.strip():
        try:
            id_asignatura = int(id_asignatura)
        except ValueError:
            id_asignatura = None
    else:
        id_asignatura = None
    
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
    if nombre or id_profesor is not None or id_asignatura is not None or precio_min is not None or precio_max is not None or capacidad_min is not None:
        asignaturas = search_asignaturas(
            nombre=nombre,
            id_profesor=id_profesor,
            id_asignatura=id_asignatura,
            precio_min=precio_min,
            precio_max=precio_max,
            capacidad_min=capacidad_min,
            offset=offset,
            limit=limit
        )
        search_active = True
    else:
        asignaturas = search_asignaturas(offset=offset, limit=limit)
        search_active = False
    
    # 4. Renderizado
    return render_template(
        "asignaturas.html",
        asignaturas=asignaturas,
        search_active=search_active,
        page=page,
        limit=limit,
        nombre=nombre,
        id_profesor=id_profesor,
        id_asignatura=id_asignatura,
        precio_min=precio_min,
        precio_max=precio_max,
        capacidad_min=capacidad_min
    )

@asignaturas_bp.route("/<int:id_asignatura>")
def view_asignatura(id_asignatura):
    print("ID recibido:", id_asignatura)

    asignatura = get_asignaturas_by_id(id_asignatura)
    alumnos = get_alumnos_by_asignatura(id_asignatura)
    area = get_asignatura_area(id_asignatura)

    return render_template(
        "idAsignatura.html",
        asignatura=asignatura,
        alumnos=alumnos,
        area=area
    )

@asignaturas_bp.route("/<int:id_asignatura>/editar-poligono", methods=["GET", "POST"])
def editar_poligono(id_asignatura):
    asignatura = get_asignaturas_by_id(id_asignatura)
    if not asignatura:
        return "Asignatura no encontrada", 404

    area_actual = get_asignatura_area(id_asignatura)
    error = None
    exito = None

    if request.method == "POST":
        polygon_text = request.form.get("polygon", "").strip()
        if not polygon_text:
            error = "El polígono no puede estar vacío."
        else:
            try:
                upsert_asignatura_poligono(id_asignatura, polygon_text)
                exito = "Polígono actualizado correctamente."
                area_actual = polygon_text
            except Exception as e:
                error = f"Error al guardar el polígono: {str(e)}"

    return render_template(
        "editarPoligono.html",
        asignatura=asignatura,
        area_actual=area_actual,
        error=error,
        exito=exito
    )

@asignaturas_bp.route("/nuevo", methods=["GET", "POST"])
def new_asignatura():
    profesores = get_profesores()
    if request.method == "POST":
        nombres = {
        "es" : request.form["nombre_es"],
        "en" : request.form["nombre_en"]}
        id_profesor = request.form["id_profesor"]
        capacidad_max = int(request.form["capacidad_max"])
        precio = float(request.form["precio"])
            
        if precio < 0:
            return "Error: El precio no puede ser negativo", 400 
        asignatura_id = crear_asignatura(nombres, id_profesor, capacidad_max, precio)

        if asignatura_id: 
            return redirect(url_for("asignaturas.view_asignatura", id_asignatura=asignatura_id))
        else:
            return "Error al crear el asignatura en la base de datos", 500
    
    return render_template("crearAsignatura.html", profesores=profesores)

@asignaturas_bp.route("/modificar/<int:id_asignatura>", methods=["GET", "POST"])
def edit_asignatura(id_asignatura):
    if request.method == "POST":
        nombres = {"es" : request.form["nombre_asignatura_es"],
        "en" : request.form["nombre_asignatura_en"]}
        id_prof = request.form["id_profesor"]
        precio = float(request.form["precio"])
        capacidad = int(request.form["capacidad_max"])

        if modificar_asignatura(id_asignatura, nombres, id_prof, precio, capacidad):
            return redirect(url_for("asignaturas.view_asignatura", id_asignatura = id_asignatura))
        else:
            return "Error al actualizar asignatura", 500

    asignatura_obj = get_asignaturas_by_id(id_asignatura)
    profs = get_profesores()
    
    if not asignatura_obj:
        return "Asignatura no encontrado", 404
        
    return render_template("modificarAsignatura.html", asignatura=asignatura_obj, profesores=profs)

@asignaturas_bp.route("/eliminar/<int:id_asignatura>", methods=["GET", "POST"])
def eliminar_asignatura(id_asignatura):
    asignatura = get_asignaturas_by_id(id_asignatura)
    if request.method == "POST":
        eliminacion = delete_asignatura(id_asignatura)
        if eliminacion:
            return redirect (url_for("asignaturas.list_",))
    
    if not asignatura:
        return "Asignatura no encontrado", 404
        
    return render_template("eliminarAsignatura.html", asignatura=asignatura)

@asignaturas_bp.route("/auditoria")
def auditoria_asignaturas():
    aud_asignaturas = view_audit_asignaturas()
    return render_template("audAsignatura.html", aud = aud_asignaturas)

@asignaturas_bp.route("/dinero")
def dinero():
    resultado = dinero_recaudado_asignatura_y_profesor()
    return render_template("dineroRecaud.html", result = resultado)

@asignaturas_bp.route("/reporte-capacidades")
def reporte_capacidades():
    resultado = capacidad_total_rollup()
    return render_template("reporteRollup.html", result=resultado)

@asignaturas_bp.route("/estadisticas-precios")
def estadisticas_precios():
    resultado = estadisticas_asignaturas_filter()
    return render_template("reporteFilter.html", result=resultado)