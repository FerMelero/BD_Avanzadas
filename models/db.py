from __future__ import annotations

import psycopg

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
                "SELECT id_curso, nombre_curso, id_profesor, precio, capacidad_max FROM cursos ORDER BY id_curso;"
            )
            return [Cursos(*r) for r in cur.fetchall()]

def get_matriculas():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id_alumno, id_curso FROM matriculas ORDER BY id_alumno;"
            )
            return [Matriculas(*r) for r in cur.fetchall()]

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
                SELECT c.id_curso, c.nombre_curso, c.id_profesor, c.precio, c.capacidad_max
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
            "SELECT id_curso, nombre_curso, id_profesor, precio, capacidad_max FROM cursos WHERE id_profesor=%s;",
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
            "SELECT id_curso, nombre_curso, id_profesor, precio, capacidad_max FROM cursos WHERE id_curso=%s;",
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
                cur.execute("SELECT nombre_curso, precio, capacidad_max FROM cursos WHERE id_curso=%s FOR UPDATE;", (id_curso,))
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
    SELECT operacion, stamp, user_id, nombre_profesor, id_profesor, dni_profesor 
    FROM audit_profesores 
    ORDER BY stamp DESC;
""")
            return [AuditProfesor(*r) for r in cur.fetchall()]

def view_audit_alumnos():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT operacion, stamp, user_id, nombre_alumno, id_alumno, dni_alumno
                FROM audit_alumnos 
                ORDER BY stamp DESC;
            """)
            return [AuditAlumno(*r) for r in cur.fetchall()]

def view_audit_cursos():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT operacion, stamp, user_id, nombre_curso, id_curso, precio_curso
                FROM audit_cursos 
                ORDER BY stamp DESC;
            """)
            return [AuditCurso(*r) for r in cur.fetchall()]

def crear_curso(nombre_curso, id_profesor, precio, capacidad_max):
    with get_connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute("""
                    INSERT INTO cursos (nombre_curso, id_profesor, precio, capacidad_max) 
                    VALUES (%s, %s, %s, %s) RETURNING id_curso;
                """, (nombre_curso, id_profesor, precio, capacidad_max))
                
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
                    SET nombre_curso = %s, id_profesor = %s, precio = %s, capacidad_max = %s
                    WHERE id_curso = %s;
                """, (nombre, id_profesor, precio, capacidad, id_curso))
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
# si se desean ver los reesultados de estos prints, ejecutar con python -m models.db desde la raíz
if __name__ == "__main__":
    print(cursos_alumnos_by_profesor(20))
    print(resumen_alumno(20))
    print(view_audit_alumnos())