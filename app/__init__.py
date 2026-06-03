from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['JSON_AS_ASCII'] = False
    from .routes import main
    app.register_blueprint(main)
    return app
