import subprocess
import sys
from backend.models import db, User, Role, GitUser
from backend.config import DevelopmentConfig
from backend.security import datastore
from backend.resources import api
from backend.instance import cache
from backend.other_api import other_api_bp

def install(package):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    except Exception as e:
        print(f"Failed to install package '{package}': {e}")
        sys.exit(1)

try:
    from flask import Flask
    from flask_security import SQLAlchemyUserDatastore, Security
    import logging
    from flask import Flask, request, jsonify
    from flask_security import current_user
    from backend.models import db, User
    from functools import wraps
except ImportError as e:
    missing_module = str(e).split("'")[1]  # Extracting the missing module's name
    print(f"Module '{missing_module}' is missing. Installing...")
    install(missing_module)
    print(f"Module '{missing_module}' installed successfully. Please restart the script.")


def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    db.init_app(app)
    api.init_app(app)
    datastore = SQLAlchemyUserDatastore(db,User,Role)
    app.security = Security(app, datastore)

    with app.app_context():
        import backend.views

    return app


app = create_app()

# List of endpoints where authentication is not required
EXEMPTED_ENDPOINTS = ['/','/user-login', '/user-signup','/favicon.ico']

# Decorator to skip authentication for exempted endpoints
def exempt_from_auth(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

# @app.before_request
def before_request():
    print(202, request.path)
    if request.path in EXEMPTED_ENDPOINTS:
        return 
    token = request.headers.get('auth-token')
    print(101,token)
    if not token:
        return jsonify({"message": "Authorization token is missing!"}), 401



app.register_blueprint(other_api_bp)
if __name__ == '__main__':
    app.run(debug=True)
