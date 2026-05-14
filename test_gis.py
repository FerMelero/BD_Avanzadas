#!/usr/bin/env python3
"""
Script de prueba para verificar que la funcionalidad GIS funciona correctamente.
"""

from models.db import (
    get_alumnos,
    get_asignaturas_con_area,
    get_alumno_ubicacion,
    get_asignatura_area,
    viajar_alumno_a_aula,
)

def test_gis():
    print("🧪 Probando funcionalidad GIS...\n")

    # 1. Verificar que hay alumnos con ubicaciones
    alumnos = get_alumnos()
    alumnos_con_ubicacion = []
    for alumno in alumnos[:10]:  # Solo primeros 10 para no saturar
        ubicacion = get_alumno_ubicacion(alumno.id_alumno)
        if ubicacion:
            alumnos_con_ubicacion.append((alumno, ubicacion))

    print(f"✅ Alumnos con ubicaciones: {len(alumnos_con_ubicacion)}")
    if alumnos_con_ubicacion:
        alumno, ubicacion = alumnos_con_ubicacion[0]
        print(f"   Ejemplo: Alumno {alumno.id_alumno} ({alumno.nombre}) en {ubicacion}")

    # 2. Verificar que hay asignaturas con polígonos
    asignaturas_con_area = get_asignaturas_con_area()
    print(f"\n✅ Asignaturas con polígonos: {len(asignaturas_con_area)}")
    for asignatura in asignaturas_con_area:
        print(f"   ID {asignatura['id_asignatura']}: {asignatura['nombres_multi']['es']}")

    # 3. Probar el método "Viajar"
    if alumnos_con_ubicacion and asignaturas_con_area:
        alumno = alumnos_con_ubicacion[0][0]
        asignatura = asignaturas_con_area[0]

        ubicacion_antes = get_alumno_ubicacion(alumno.id_alumno)
        print(f"\n🎯 Probando 'Viajar' para alumno {alumno.id_alumno}")
        print(f"   Ubicación antes: {ubicacion_antes}")

        resultado = viajar_alumno_a_aula(alumno.id_alumno, asignatura['id_asignatura'])
        if resultado is True:
            ubicacion_despues = get_alumno_ubicacion(alumno.id_alumno)
            print(f"   Ubicación después: {ubicacion_despues}")
            print("   ✅ Viaje exitoso!")
        else:
            print(f"   ❌ Error en viaje: {resultado}")

    print("\n🎉 Pruebas completadas!")

if __name__ == "__main__":
    test_gis()
