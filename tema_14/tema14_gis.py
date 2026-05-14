from models.db import (
    get_alumnos,
    get_asignaturas,
    upsert_alumno_ubicacion,
    upsert_asignatura_poligono,
    get_asignatura_area,
    get_alumno_ubicacion,
)

SAMPLE_PUNTOS = [
    "(2.1700,41.3851)",   # Barcelona
    "(-3.7038,40.4168)",  # Madrid
    "(-0.3763,39.4699)",  # Valencia
    "(-0.4890,38.3452)",  # Alicante
    "(2.1734,41.3851)",   # Barcelona 2
    "(-3.6923,40.4168)",  # Madrid 2
    "(-0.3773,39.4699)",  # Valencia 2
    "(-0.4880,38.3452)",  # Alicante 2
]

SAMPLE_POLIGONOS = [
    "((-3.7050,40.4182),(-3.7030,40.4182),(-3.7030,40.4170),(-3.7050,40.4170),(-3.7050,40.4182))",  # Madrid
    "((2.1690,41.3861),(2.1710,41.3861),(2.1710,41.3840),(2.1690,41.3840),(2.1690,41.3861))",        # Barcelona
    "((-0.3775,39.4715),(-0.3755,39.4715),(-0.3755,39.4685),(-0.3775,39.4685),(-0.3775,39.4715))",  # Valencia
    "((-0.4830,38.3465),(-0.4870,38.3465),(-0.4870,38.3435),(-0.4830,38.3435),(-0.4830,38.3465))",  # Alicante
    "((2.1730,41.3861),(2.1750,41.3861),(2.1750,41.3840),(2.1730,41.3840),(2.1730,41.3861))",        # Barcelona 2
    "((-3.6920,40.4182),(-3.6900,40.4182),(-3.6900,40.4170),(-3.6920,40.4170),(-3.6920,40.4182))",  # Madrid 2
    "((-0.3785,39.4715),(-0.3765,39.4715),(-0.3765,39.4685),(-0.3785,39.4685),(-0.3785,39.4715))",  # Valencia 2
    "((-0.4840,38.3465),(-0.4880,38.3465),(-0.4880,38.3435),(-0.4840,38.3435),(-0.4840,38.3465))",  # Alicante 2
]


def insertar_gis_de_muestra():
    alumnos = get_alumnos()
    asignaturas = get_asignaturas()

    if not alumnos:
        print("No hay alumnos en la base de datos. Inserte alumnos primero.")
        return

    if not asignaturas:
        print("No hay asignaturas en la base de datos. Inserte asignaturas primero.")
        return

    print("\n=== Insertando ubicaciones de alumnos ===")
    # Asignar ubicaciones a alumnos que no las tengan
    alumnos_sin_ubicacion = []
    for alumno in alumnos:
        if not get_alumno_ubicacion(alumno.id_alumno):
            alumnos_sin_ubicacion.append(alumno)

    if alumnos_sin_ubicacion:
        for idx, alumno in enumerate(alumnos_sin_ubicacion[:len(SAMPLE_PUNTOS)]):
            punto = SAMPLE_PUNTOS[idx % len(SAMPLE_PUNTOS)]
            upsert_alumno_ubicacion(alumno.id_alumno, punto)
            print(f"✓ Alumno {alumno.id_alumno}: ubicación asignada {punto}")
    else:
        print("ℹTodos los alumnos ya tienen ubicaciones asignadas.")

    print("\n=== Insertando polígonos de asignaturas ===")
    # Asignar polígonos a asignaturas que no los tengan
    asignaturas_sin_poligono = []
    for asignatura in asignaturas:
        if not get_asignatura_area(asignatura.id_asignatura):
            asignaturas_sin_poligono.append(asignatura)

    if asignaturas_sin_poligono:
        for idx, asignatura in enumerate(asignaturas_sin_poligono):
            poligono = SAMPLE_POLIGONOS[idx % len(SAMPLE_POLIGONOS)]
            upsert_asignatura_poligono(asignatura.id_asignatura, poligono)
            print(f"✓ Asignatura {asignatura.id_asignatura}: polígono asignado")
    else:
        print("ℹTodas las asignaturas ya tienen polígonos asignados.")

    print(f"\nDatos GIS actualizados exitosamente.")
    print(f"   {len(alumnos)} alumnos totales, {len(alumnos) - len(alumnos_sin_ubicacion)} con ubicaciones.")
    print(f"   {len(asignaturas)} asignaturas totales, {len(asignaturas) - len(asignaturas_sin_poligono)} con polígonos.")


if __name__ == "__main__":
    insertar_gis_de_muestra()
