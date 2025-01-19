from flask import Flask
from flask_pymongo import PyMongo

def create_app():
    app = Flask(__name__)

    # Configuration for MongoDB
    app.config["MONGO_URI"] = "mongodb://localhost:27017/marketplaceDB"
    mongo = PyMongo(app)


    # Register Blueprints
    from users import users_bp
    app.register_blueprint(users_bp)

    @app.route('/')
    def home():
        return "Hello, Flask!"
    
    # Attach the mongo instance to the app context
    app.mongo = mongo

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5006, debug=True)