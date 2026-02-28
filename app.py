from __future__ import annotations
from flask import Flask, render_template
from routes import main_bp, alumnos_bp, profesores_bp, cursos_bp, matriculas_bp

def create_app() -> Flask:
    app = Flask(__name__)

    app.config["ENV"] = "development"
    app.config["SECRET_KEY"] = "dev-change-in-production"

    app.register_blueprint(main_bp)
    app.register_blueprint(alumnos_bp)
    app.register_blueprint(profesores_bp)
    app.register_blueprint(cursos_bp)
    app.register_blueprint(matriculas_bp)

    @app.errorhandler(404)
    def not_found(e):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def server_error(e):
        return render_template("errors/500.html"), 500

    return app

app = create_app()