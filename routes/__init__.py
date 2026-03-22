# Blueprints: rutas agrupadas por recurso (main, vendors, parts).

from routes.main import main_bp
from routes.alumnos import alumnos_bp
from routes.profesores import profesores_bp
from routes.cursos import cursos_bp
from routes.matriculas import matriculas_bp
from routes.auth import auth_bp


__all__ = ["main_bp", "alumnos_bp", "profesores_bp", "cursos_bp", "matriculas_bp", "auth_bp"]
