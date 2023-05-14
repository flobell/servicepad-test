from flask import Blueprint, current_app
from flask_restx import Api
from .resources import API_NAMESPACES

blueprint = Blueprint('api',__name__)

# authorizations types for routes in api
authorizations = {
    # 'apikey' : {
    #     'type' : 'apiKey',
    #     'in' : 'header',
    #     'name' : 'X-API-Key'
    # },
    'jwt' : {
        'type' : 'apiKey',
        'in' : 'header',
        'name' : 'Authorization'
    }
}

api: Api = Api(
    blueprint,
    version=current_app.config['info']['version'],
    title=current_app.config['info']['name'],
    description=current_app.config['info']['description'],
    prefix='/api',
    authorizations=authorizations,
    doc='/' if current_app.config['SWAGGER_UI_SHOW'] else False,
)


for ns in API_NAMESPACES:
    api.add_namespace(ns)    