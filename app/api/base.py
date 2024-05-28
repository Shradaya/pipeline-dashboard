from flask import Blueprint

api_router_v1 = Blueprint('api_router', __name__, url_prefix='/v1/api')

from .v1.leave import route as r1