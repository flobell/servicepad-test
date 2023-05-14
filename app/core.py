import logging, os, sys, click
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_caching import Cache
from flask_bcrypt import Bcrypt
from app.database import db
from app.exceptions import NoConfigFileException
from dependency_injector import containers, providers
from logging.config import dictConfig


def create_app(config=None):
    logging.info('Creating app.')

    if config is None:
        logging.critical('config not defined')
        raise NoConfigFileException
    
    # create flask app
    app = Flask(__name__, static_folder='static', template_folder='templates', instance_relative_config=True)

    # load config
    app.config['info'] = config['info']
    for k, v in config['web'].items():
        app.config[k] = v
    app.config['SERVER_NAME'] = f"{app.config['HOST']}:{app.config['PORT']}"

    # init dependencies
    db.init_app(app)
    app.jwt_manager = JWTManager(app)
    app.cache = Cache(app)
    app.bcrypt = Bcrypt(app)

    # init blueprints
    with app.app_context():
        from .api import blueprint
        app.register_blueprint(blueprint)

    return app


class Core(containers.DeclarativeContainer):
    config = providers.Configuration()
    log = providers.Resource(dictConfig, config=config.logging)
    app = providers.Factory(create_app, config=config)
    

def get_core_obj() -> Core:
    conf_file_path = os.getenv('APP_CONFIG')
    
    if conf_file_path is None:
        click.echo(
            click.style(
                'APP_CONFIG variable is not defined',
                fg='red',
                bold=True
            )
        )
        sys.exit(1)

    core_obj = Core()
    core_obj.config.from_yaml(conf_file_path)
    core_obj.init_resources()
    return core_obj