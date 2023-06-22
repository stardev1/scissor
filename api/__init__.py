from flask import Blueprint, jsonify

from .v1.resources.shorten_url import shortener
from .v1.resources.user import user
from .v1.resources.auth import authRoute

apiRoutes = Blueprint('api', __name__, url_prefix="/api")



def api_error_handler_404(e):
        return jsonify({
            "status": "error",
            "message": "url not found"
        }), 404 

apiRoutes.register_error_handler(404, api_error_handler_404)


apiRoutes.register_blueprint(authRoute)

apiRoutes.register_blueprint(shortener)

apiRoutes.register_blueprint(user)
