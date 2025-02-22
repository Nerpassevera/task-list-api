from flask_cors import CORS
from flask import Flask
import os
from .routes.task_routes import bp as task_bp
from .routes.goal_routes import bp as goal_bp
from .db import db, migrate
from .models import task, goal


def create_app(config=None):
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": [
        "http://localhost:5173",
        "https://task-list-api-a1l3.onrender.com",
        "https://nerpassevera.github.io"
    ]}})
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        'SQLALCHEMY_DATABASE_URI')

    if config:
        # Merge `config` into the app's configuration
        # to override the app's default settings for testing
        app.config.update(config)

    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints here
    app.register_blueprint(task_bp)
    app.register_blueprint(goal_bp)

    return app
