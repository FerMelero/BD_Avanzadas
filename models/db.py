from __future__ import annotations

import psycopg
import json

from config import load_config

from models.entities import Alumno, Profesor, Matriculas, Cursos, AuditProfesor, AuditAlumno, AuditCurso

def get_connection():
    cfg = load_config()
    return psycopg.connect(**cfg)

def get_alumnos():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id_alumno, nombre, apellido, fecha_nacimiento, dni, dinero FROM alumnos ORDER BY id_alumno;"
            )
            return [Alumno(*r) for r in cur.fetchall()]

def get_profesores():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id_profesor, nombre, apellido, fecha_nacimiento, dni FROM profesores ORDER BY id_profesor;"
            )
            return [Profesor(*r) for r in cur.fetchall()]

def get_cursos():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id_curso, nombres_multi, id_profesor, precio, capacidad_max FROM cursos ORDER BY id_curso;"
            )
            return [Cursos(*r) for r in cur.fetchall()]

def get_matriculas():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id_alumno, id_curso FROM matriculas ORDER BY id_alumno;"
            )
            return [Matriculas(*r) for r in cur.fetchall()]


def get_matriculas_vista():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT nombre_alumno, nombre_profesor, nombre_curso FROM vista_alumnos_profesores_cursos ORDER BY nombre_alumno, nombre_curso;"
            )
            return [
                {
                    "nombre_alumno": row[0],
                    "nombre_profesor": row[1],
                    "nombre_curso": row[2],
                }
                for row in cur.fetchall()
            ]


def get_alumno_by_id(id_alumno): # pasamos un ID específico
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
            "SELECT id_alumno, nombre, apellido, fecha_nacimiento, dni ,dinero FROM alumnos WHERE id_alumno=%s;",
            (id_alumno,) # debemos poner %s(id_alumno, ) para que seleccione bien el ID
        )
            row = cur.fetchone()
            print("Fila obtenida:", row) # depuración
            if row:
                return Alumno(*row) # ahora solo se devuelve un objeto que es una fila
            return None


def get_cursos_by_alumno(id_alumno):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT c.id_curso, c.nombres_multi, c.id_profesor, c.precio, c.capacidad_max
                FROM cursos c
                JOIN matriculas m ON c.id_curso = m.id_curso
                WHERE m.id_alumno = %s;
                """,
                (id_alumno,)
            )

            rows = cur.fetchall()
            print("Cursos obtenidos:", rows)

            return [Cursos(*r) for r in rows]


def get_profesor_by_id(id_profesor): # pasamos un ID específico
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
            "SELECT p.id_profesor, p.nombre, p.apellido, p.fecha_nacimiento, p.dni FROM profesores p WHERE p.id_profesor=%s;",
            (id_profesor,) # debemos poner %s(id_profesor, ) para que seleccione bien el ID
        )
            row = cur.fetchone()
            print("Fila obtenida:", row) # depuración
            if row:
                return Profesor(*row) # ahora solo se devuelve un objeto que es una fila
            return None

def get_cursos_by_profesor(id_profesor): # pasamos un ID específico
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
            "SELECT id_curso, nombres_multi, id_profesor, precio, capacidad_max FROM cursos WHERE id_profesor=%s;",
            (id_profesor,) # debemos poner %s(id_profesor, ) para que seleccione bien el ID
        )
            rows = cur.fetchall()
            print("Fila obtenida:", rows) # depuración
            return [Cursos(*r) for r in rows]

def get_cursos_by_id(id_curso):
    with get_connection() as conn:
        with conn.cursor() as cur:
            print("Buscando curso con id:", id_curso)
            cur.execute(
            "SELECT id_curso, nombres_multi, id_profesor, precio, capacidad_max FROM cursos WHERE id_curso=%s;",
            (id_curso,) # debemos poner %s(id_curso, ) para que seleccione bien el ID
        )
            row = cur.fetchone()
            print("Fila obtenida:", row) # depuración
            if row:
                return Cursos(*row) # ahora solo se devuelve un objeto que es una fila
            return None

def get_alumnos_by_curso(id_curso):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
            "SELECT a.id_alumno, a.nombre, a.apellido, a.fecha_nacimiento, a.dni, a.dinero FROM alumnos a JOIN matriculas m ON a.id_alumno = m.id_alumno WHERE m.id_curso=%s;",
            (id_curso,) # debemos poner %s(id_curso, ) para que seleccione bien el ID
        )
            rows = cur.fetchall()
            print("Fila obtenida:", rows) # depuración
            return [Alumno(*r) for r in rows]

def crear_alumno(nombre, apellidos, fecha_nacimiento_alumno, dni, dinero):
    with get_connection() as conn:
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO alumnos (nombre, apellido, fecha_nacimiento, dni, dinero) VALUES (%s, %s, %s, %s, %s) RETURNING id_alumno;",
                    (nombre, apellidos, fecha_nacimiento_alumno, dni, dinero)
                )
                id_alumno = cur.fetchone()[0]
                conn.commit()
                return id_alumno
        except Exception as e:
            conn.rollback()
            print(f"Error al crear alumno: {e}")
            return None

def crear_matricula(id_alumno: int, id_curso: int):
    with get_connection() as conn:
        with conn.cursor() as cur:
            try:
                # primero sacamos los datos del alumno
                cur.execute("SELECT nombre, dinero FROM alumnos WHERE id_alumno=%s FOR UPDATE;", 
                (id_alumno,))
                alumno = cur.fetchone() # recuperar el dato
            
                if not alumno:
                    return "Alumno no encontrado"
                
                nombre_alumno, dinero = alumno # si existe el alumno, guardamos y seguimos

                # ahora sacamos los datos del curso
                cur.execute("SELECT nombres_multi, precio, capacidad_max FROM cursos WHERE id_curso=%s FOR UPDATE;", (id_curso,))
                curso = cur.fetchone()

                if not curso:
                    return "Curso no encontrado"

                nombre_curso, precio_curso, capacidad_max = curso

                # verificamos que el alumno no esté matriculado ya
                cur.execute("SELECT 1 FROM matriculas WHERE id_alumno=%s AND id_curso=%s;", (id_alumno, id_curso,))
                if cur.fetchone(): # si obtenemos resultado de que está matriculado
                    return f"EL alumno {nombre_alumno} ya está matriculado en {nombre_curso}"
                
                # comprobar que el curso tiene plazas
                cur.execute("SELECT COUNT(*) FROM matriculas WHERE id_curso=%s;", (id_curso,))
                actuales = cur.fetchone()[0]
                if actuales >= capacidad_max:
                    return f"El curso {nombre_curso} está lleno ({capacidad_max} plazas máx.)"

                # verificar que el alumno tiene el saldo suficiente
                if dinero < precio_curso:
                    return f"Saldo insuficiente. EL alumno {nombre_alumno} tiene {dinero}€ y el curso son {precio_curso}€"
                
                # una vez comprobado todo acutalizamos su saldo
                cur.execute(
                    "UPDATE alumnos SET dinero = dinero - %s WHERE id_alumno = %s;", 
                    (precio_curso, id_alumno)
                )
                
                # insertamos finalmente la matrícula
                cur.execute(
                    "INSERT INTO matriculas (id_alumno, id_curso) VALUES (%s, %s);",
                    (id_alumno, id_curso)
                )
                conn.commit()
                return True
            except Exception as e:
                conn.rollback()
                return f"Error: {str(e)}"

def demo_transaccion_rollback():
    conn = get_connection()

    try:
        cur = conn.cursor()

        # insert válido
        cur.execute(
            "INSERT INTO matriculas (id_alumno, id_curso) VALUES (%s, %s);",
            (1, 1)
        )

        # este insert falla
        cur.execute(
            "INSERT INTO matriculas (id_alumno, id_curso) VALUES (%s, %s);",
            (1, 9999)
        )

        conn.commit()

    except Exception as e:
        conn.rollback()
        print("Rollback ejecutado:", e)

    finally:
        cur.close()
        conn.close()

def cursos_alumnos_by_profesor(id_profesor):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT 
                    COUNT(DISTINCT c.id_curso) AS num_cursos,
                    COUNT(DISTINCT m.id_alumno) AS num_alumnos
                FROM cursos c
                LEFT JOIN matriculas m ON c.id_curso = m.id_curso
                WHERE c.id_profesor = %s;
            """, (id_profesor,))

            row = cur.fetchone()
            return {
                "num_cursos": row[0],
                "num_alumnos_distintos": row[1]
            }

def resumen_alumno(id_alumno):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT 
                    COUNT(DISTINCT m.id_curso) AS num_cursos,
                    COUNT(DISTINCT c.id_profesor) AS num_profesores
                FROM matriculas m
                JOIN cursos c ON m.id_curso = c.id_curso
                WHERE m.id_alumno = %s;
            """, (id_alumno,))

            row = cur.fetchone()
            return {
                "num_cursos": row[0],
                "num_profesores_distintos": row[1]
            }

def view_audit_profesores():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT operacion, stamp, user_id, id_profesor, nombre, apellido, fecha_nacimiento, dni 
                FROM audit_profesores 
                ORDER BY stamp DESC;
            """)
            return [AuditProfesor(*r) for r in cur.fetchall()]

def view_audit_alumnos():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT operacion, stamp, user_id, id_alumno, nombre, apellido, fecha_nacimiento, dni, dinero
                FROM audit_alumnos 
                ORDER BY stamp DESC;
            """)
            return [AuditAlumno(*r) for r in cur.fetchall()]

def view_audit_cursos():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT operacion, stamp, user_id, id_curso, nombres_multi, id_profesor, capacidad_max, precio
                FROM audit_cursos 
                ORDER BY stamp DESC;
            """)
            return [AuditCurso(*r) for r in cur.fetchall()]

def crear_curso(nombres_multi, id_profesor, precio, capacidad_max):
    with get_connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute("""
                INSERT INTO cursos (nombres_multi, id_profesor, capacidad_max, precio)
                VALUES (%s, %s, %s, %s) RETURNING id_curso;
            """, (psycopg.types.json.Jsonb(nombres_multi), id_profesor, capacidad_max, precio))
                
                id_curso = cur.fetchone()[0]
                conn.commit()
                return id_curso
            except Exception as e:
                conn.rollback()
                print(f"Error al crear curso: {e}") 
                return None

def crear_profesor(nombre, apellido, fecha_nac, dni):
    with get_connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute(""" INSERT INTO profesores (nombre, apellido, fecha_nacimiento, dni) 
                    VALUES (%s, %s, %s, %s) RETURNING id_profesor;                
            """, (nombre, apellido, fecha_nac, dni))
                
                id_profesor = cur.fetchone()[0]
                conn.commit()
                return id_profesor

            except Exception as e:
                conn.rollback()
                print(f"Error al crear profesor: {e}") 
                return None

def modificar_alumno(id_alumno, nombre, apellido, fecha_nacimiento, dni, dinero):
    with get_connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute(
                    "UPDATE alumnos SET nombre = %s, apellido = %s, fecha_nacimiento = %s, dni = %s, dinero = %s WHERE id_alumno = %s;", 
                    (nombre, apellido, fecha_nacimiento, dni, dinero, id_alumno,)
                )
                conn.commit()
                return True

            except Exception as e:
                conn.rollback()
                print(f"Error al mdoficar alumno: {e}") 
                return None

def modificar_profesor(id_profesor, nombre, apellido, fecha_nacimiento, dni):
    with get_connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute(
                    "UPDATE profesores SET nombre = %s, apellido = %s, fecha_nacimiento = %s, dni = %s WHERE id_profesor = %s;", 
                    (nombre, apellido, fecha_nacimiento, dni, id_profesor,)
                )
                conn.commit()
                return True

            except Exception as e:
                conn.rollback()
                print(f"Error al mdoficar profesor: {e}") 
                return None




def modificar_curso(id_curso, nombre, id_profesor, precio, capacidad):
    with get_connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute("""
                    UPDATE cursos 
                    SET nombres_multi = %s, id_profesor = %s, precio = %s, capacidad_max = %s
                    WHERE id_curso = %s;
                """, (psycopg.types.json.Jsonb(nombre), id_profesor, precio, capacidad, id_curso))
                conn.commit()
                return True
            except Exception as e:
                conn.rollback()
                print(f"Error al modificar curso: {e}")
                return False

def delete_alumno(id_alumno):
    with get_connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute(
                    "DELETE FROM alumnos WHERE id_alumno = %s;", 
                    (id_alumno,)
                )
                conn.commit()
                return True

            except Exception as e:
                conn.rollback()
                print(f"Error al eliminar el alumno alumno: {e}") 
                return None

def delete_profesor(id_profesor):
    with get_connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute(
                    "DELETE FROM profesores WHERE id_profesor = %s;", 
                    (id_profesor,)
                )
                conn.commit()
                return True

            except Exception as e:
                conn.rollback()
                print(f"Error al eliminar el profesor: {e}") 
                return None

def delete_curso(id_curso):
    with get_connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute(
                    "DELETE FROM cursos WHERE id_curso = %s;", 
                    (id_curso,)
                )
                conn.commit()
                return True

            except Exception as e:
                conn.rollback()
                print(f"Error al eliminar el curso: {e}") 
                return None

# ============================================
# BÚSQUEDAS FILTRADAS Y SEGURAS (Tema 12)
# ============================================

def search_alumnos(nombre=None, apellido=None, dni=None, dinero_min=None, dinero_max=None, offset=0, limit=10):
    """Búsqueda segura y parametrizada de alumnos con filtros string, numéricos y paginación."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            sql = "SELECT id_alumno, nombre, apellido, fecha_nacimiento, dni, dinero FROM alumnos WHERE 1=1"
            params = []
            
            # Normalizar entradas string vacías a None
            if nombre is not None:
                nombre = nombre.strip() or None
            if apellido is not None:
                apellido = apellido.strip() or None
            if dni is not None:
                dni = dni.strip() or None
            
            # Filtro por nombre (ILIKE insensible a mayúsculas, como en tema12)
            if nombre:
                sql += " AND nombre ILIKE %s"
                params.append(f"%{nombre}%")
            
            # Filtro por apellido
            if apellido:
                sql += " AND apellido ILIKE %s"
                params.append(f"%{apellido}%")
            
            # Filtro por DNI
            if dni:
                sql += " AND dni ILIKE %s"
                params.append(f"%{dni}%")
            
            # Filtro por dinero mínimo
            if dinero_min is not None:
                sql += " AND dinero >= %s"
                params.append(dinero_min)
            
            # Filtro por dinero máximo
            if dinero_max is not None:
                sql += " AND dinero <= %s"
                params.append(dinero_max)
            
            # Ordenamiento + paginación
            sql += " ORDER BY id_alumno LIMIT %s OFFSET %s"
            params.extend([limit, offset])
            
            cur.execute(sql, params)
            return [Alumno(*r) for r in cur.fetchall()]

def search_profesores(nombre=None, apellido=None, dni=None, fecha_nacimiento=None, offset=0, limit=10):
    """Búsqueda segura y parametrizada de profesores con filtros string, numéricos y paginación."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            sql = "SELECT id_profesor, nombre, apellido, fecha_nacimiento, dni FROM profesores WHERE 1=1"
            params = []
            
            if nombre:
                sql += " AND nombre ILIKE %s"
                params.append(f"%{nombre}%")
            
            if apellido:
                sql += " AND apellido ILIKE %s"
                params.append(f"%{apellido}%")
            
            if dni:
                sql += " AND dni ILIKE %s"
                params.append(f"%{dni}%")
            
            if fecha_nacimiento:
                sql += " AND fecha_nacimiento = %s"
                params.append(fecha_nacimiento)
            
            sql += " ORDER BY id_profesor LIMIT %s OFFSET %s"
            params.extend([limit, offset])
            
            cur.execute(sql, params)
            return [Profesor(*r) for r in cur.fetchall()]

def search_cursos(nombre=None, precio_min=None, precio_max=None, capacidad_min=None, id_profesor=None, id_curso=None, offset=0, limit=10):
    """Búsqueda segura y parametrizada de cursos con filtros string, numéricos, IDs y paginación."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            sql = "SELECT id_curso, nombres_multi, id_profesor, precio, capacidad_max FROM cursos WHERE 1=1"
            params = []
            
            if nombre:
                
                sql += """ AND (
                    unaccent(nombres_multi->>'es') ILIKE unaccent(%s) OR 
                    unaccent(nombres_multi->>'en') ILIKE unaccent(%s) OR
                    unaccent(nombres_multi->>'es') %% unaccent(%s)
                )"""
                termino_like = f"%{nombre}%"
                params.append(termino_like) 
                params.append(termino_like) 
                params.append(nombre)
            
            if precio_min is not None:
                sql += " AND precio >= %s"
                params.append(precio_min)
            
            if precio_max is not None:
                sql += " AND precio <= %s"
                params.append(precio_max)
            
            if capacidad_min is not None:
                sql += " AND capacidad_max >= %s"
                params.append(capacidad_min)
            
            if id_profesor is not None:
                sql += " AND id_profesor = %s"
                params.append(id_profesor)
            
            if id_curso is not None:
                sql += " AND id_curso = %s"
                params.append(id_curso)
            
            if nombre:
                sql += " ORDER BY similarity(unaccent(nombres_multi->>'es'), unaccent(%s)) DESC"
                params.append(nombre)
            else:
                sql += " ORDER BY id_curso"
                
            sql += " LIMIT %s OFFSET %s"
            params.extend([limit, offset])
            
            cur.execute(sql, params)
            return [Cursos(*r) for r in cur.fetchall()]

def search_matriculas(id_curso=None, id_alumno=None, offset=0, limit=10):
    """Búsqueda segura y parametrizada de matriculas con filtros y paginación."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            sql = """
                SELECT m.id_alumno, m.id_curso, a.nombre, a.apellido, c.nombres_multi, c.precio
                FROM matriculas m
                JOIN alumnos a ON m.id_alumno = a.id_alumno
                JOIN cursos c ON m.id_curso = c.id_curso
                WHERE 1=1
            """
            params = []
            
            if id_curso is not None:
                sql += " AND m.id_curso = %s"
                params.append(id_curso)
            
            if id_alumno is not None:
                sql += " AND m.id_alumno = %s"
                params.append(id_alumno)
            
            sql += " ORDER BY m.id_alumno LIMIT %s OFFSET %s"
            params.extend([limit, offset])
            
            cur.execute(sql, params)
            # Devolver como diccionarios para mayor flexibilidad
            return cur.fetchall()

def search_matriculas_vista(nombre_alumno=None, nombre_profesor=None, nombre_curso=None, offset=0, limit=10):
    """Búsqueda segura y parametrizada en la vista alumnos-profesores-cursos."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            sql = """
                SELECT nombre_alumno, nombre_profesor, nombre_curso 
                FROM vista_alumnos_profesores_cursos 
                WHERE 1=1
            """
            params = []
            
            if nombre_alumno:
                sql += " AND nombre_alumno ILIKE %s"
                params.append(f"%{nombre_alumno}%")
            
            if nombre_profesor:
                sql += " AND nombre_profesor ILIKE %s"
                params.append(f"%{nombre_profesor}%")
            
            if nombre_curso:
                sql += " AND nombre_curso ILIKE %s"
                params.append(f"%{nombre_curso}%")
            
            sql += " ORDER BY nombre_alumno, nombre_curso LIMIT %s OFFSET %s"
            params.extend([limit, offset])
            
            cur.execute(sql, params)
            return [
                {
                    "nombre_alumno": row[0],
                    "nombre_profesor": row[1],
                    "nombre_curso": row[2],
                }
                for row in cur.fetchall()
            ]

# esta consulta usa row_number para asignar el puesto en la lista
def curso_caro_by_profesor(id_profesor):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''SELECT p.nombre AS profesor,
                        c.nombres_multi->>'es' AS curso, c.precio,
                        ROW_NUMBER() OVER (PARTITION BY p.id_profesor ORDER BY c.precio DESC) AS ranking_precio
                        FROM profesores p
                        JOIN cursos c ON p.id_profesor = c.id_profesor WHERE p.id_profesor=%s;''', (id_profesor,))
            
            rows = cur.fetchall()
            print("Fila obtenida:", rows) # depuración
            return rows

def dinero_recaudado_curso_y_profesor():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                SELECT 
                    p.nombre AS profesor,
                    c.nombres_multi->>'es' AS curso,
                    SUM(c.precio) AS recaudacion_total
                FROM profesores p
                JOIN cursos c ON p.id_profesor = c.id_profesor
                GROUP BY GROUPING SETS (
                    (p.nombre, c.nombres_multi->>'es'), 
                    (p.nombre),                         
                    ()                                  
                );
            ''',)
            
            rows = cur.fetchall()
            return rows

def capacidad_total_rollup():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                SELECT 
                    p.nombre AS profesor,
                    c.nombres_multi->>'es' AS curso,
                    SUM(c.capacidad_max) AS capacidad_total
                FROM profesores p
                JOIN cursos c ON p.id_profesor = c.id_profesor
                GROUP BY ROLLUP (p.nombre, c.nombres_multi->>'es')
                ORDER BY p.nombre NULLS LAST, curso NULLS LAST;
            ''')
            return cur.fetchall()

def estadisticas_cursos_filter():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                SELECT 
                    p.nombre AS profesor,
                    COUNT(c.id_curso) AS total_cursos,
                    COUNT(c.id_curso) FILTER (WHERE c.precio > 80) AS cursos_premium,
                    COUNT(c.id_curso) FILTER (WHERE c.precio <= 80) AS cursos_estandar
                FROM profesores p
                JOIN cursos c ON p.id_profesor = c.id_profesor
                GROUP BY p.nombre
                ORDER BY p.nombre;
            ''')
            return cur.fetchall()
# si se desean ver los reesultados de estos prints, ejecutar con python -m models.db desde la raíz
if __name__ == "__main__":
    print(curso_caro_by_profesor(1))