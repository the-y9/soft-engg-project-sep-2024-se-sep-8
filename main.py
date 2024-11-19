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
app.register_blueprint(other_api_bp)
if __name__ == '__main__':
    app.run(debug=True)