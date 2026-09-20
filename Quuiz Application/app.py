"""
Main Flask Application entry point for Quiz Application (Feature Set B).
College Project — BCA 3rd Semester Python Subject.
"""

import os
from flask import Flask, render_template
from config import Config
from routes.quiz_routes import quiz_bp
from routes.result_routes import result_bp


def create_app(config_class=Config):
    """
    Application factory for the Flask Quiz Application.
    Configures settings, registers blueprints, and hooks error handlers.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Register blueprints
    app.register_blueprint(quiz_bp)
    app.register_blueprint(result_bp)
    
    # Custom Error Handlers
    @app.errorhandler(400)
    def bad_request_error(error):
        return render_template(
            "error.html",
            error_code=400,
            error_title="Bad Request",
            error_message="The request could not be processed due to invalid syntax or parameters."
        ), 400

    @app.errorhandler(404)
    def not_found_error(error):
        return render_template(
            "error.html",
            error_code=404,
            error_title="Page Not Found",
            error_message="The page or route you are looking for does not exist."
        ), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return render_template(
            "error.html",
            error_code=500,
            error_title="Internal Server Error",
            error_message="An unexpected server error occurred. Please try restarting the quiz."
        ), 500

    return app


app = create_app()

if __name__ == "__main__":
    # Ensure database exists before launching
    from database.seed import init_database
    init_database()
    
    port = int(os.environ.get("PORT", 5000))
    print(f"\n=======================================================")
    print(f" Quiz Application (Feature Set B) — Ready!")
    print(f" Localhost URL: http://127.0.0.1:{port}")
    print(f" Press CTRL+C to quit")
    print(f"=======================================================\n")
    app.run(host="127.0.0.1", port=port, debug=True)
