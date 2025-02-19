# Import and patch all supported libraries for Datadog APM
from ddtrace import tracer

from flask import Flask
from flask_pymongo import PyMongo

def create_app():
    """
    Creates and configures the Flask application, sets up MongoDB, 
    and registers the 'users' blueprint.
    """
    app = Flask(__name__)

    # Configuration for MongoDB
    app.config["MONGO_URI"] = "mongodb://localhost:27017/marketplaceDB"
    mongo = PyMongo(app)


    # Register Blueprints
    from users import users_bp
    app.register_blueprint(users_bp)

    @app.route('/')
    @tracer.wrap('flask.request', service='flask', resource='home', span_type='web')
    def home():
        return "Hello, Flask!"
    
    # Attach the mongo instance to the app context
    app.mongo = mongo

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5006, debug=True)