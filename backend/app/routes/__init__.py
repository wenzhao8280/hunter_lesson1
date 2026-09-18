"""Blueprint registration.

Keeping this separate from app/__init__.py means the app factory doesn't
need to know the details of each blueprint, just that routes exist.
"""


def register_routes(app):
    from app.routes.schools import schools_bp
    from app.routes.cases import cases_bp

    app.register_blueprint(schools_bp)
    app.register_blueprint(cases_bp)
