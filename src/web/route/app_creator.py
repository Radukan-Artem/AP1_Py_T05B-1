from flask import Flask

from flask_jwt_extended import JWTManager

from web.route.auth import *
from web.route.game_view import *
from di.container import Container

def create_app():
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config["JWT_TOKEN_LOCATION"] = ["headers"]
    app.config['container'] = Container()
    
    jwt = JWTManager(app)

    app.register_blueprint(auth)

    app.register_blueprint(game_view) 

    return app