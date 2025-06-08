from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf import CSRFProtect
from datetime import timedelta
from .error_handlers import register_error_handlers
import os

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'main.index'
csrf = CSRFProtect()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'CJnjhuaio8cmoai4usba2klw'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../instance/students.db'
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'uploads')
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
    app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=7)

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    migrate.init_app(app, db)

    from app.main.routes import main
    from app.auth.routes import auth
    from app.students.routes import students
    from app.admin.routes import admin_bp

    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(students)
    app.register_blueprint(admin_bp)

    register_error_handlers(app)

    return app
