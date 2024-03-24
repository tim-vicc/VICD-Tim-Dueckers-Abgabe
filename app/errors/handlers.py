from flask import render_template, request
from app import db
from app.errors import bp
from app.api.errors import error_response as api_error_response

# Prüft ob eine Json antwort erwünscht ist je nach Accept-header
def wants_json_response():
    return (
        request.accept_mimetypes["application/json"]
        >= request.accept_mimetypes["text/html"]
    )

# Behandelt den error 404, im Falle dass eine Seite inexistent ist
@bp.app_errorhandler(404)
def not_found_error(error):
    if wants_json_response():
        return api_error_response(404)
    return render_template("pages/errors/404.html"), 404

# Behandelt dern error 500 (internal server error) und macht die anpassungen an der db rückgängig damit keine Dateninkonsistenzt entsteht
@bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    if wants_json_response():
        return api_error_response(500)
    return render_template("pages/errors/500.html"), 500
