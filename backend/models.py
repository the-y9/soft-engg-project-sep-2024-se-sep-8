import subprocess
import sys


def install(package):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    except Exception as e:
        print(f"Failed to install package '{package}': {e}")
        sys.exit(1)


try:
    from flask_sqlalchemy import SQLAlchemy
    from flask_security import UserMixin, RoleMixin
    from sqlalchemy import func
    from datetime import datetime, timezone
    # from sqlalchemy import func
except ImportError as e:
    missing_module = str(e).split("'")[1]
    print(f"Module '{missing_module}' is missing. Installing...")
    install(missing_module)
    print(f"Module '{missing_module}' installed. Restart the script.")
    sys.exit(1)

db = SQLAlchemy()


class RolesUsers(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column('user_id', db.Integer(), db.ForeignKey('user.id'))
    role_id = db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String, unique=True)
    username = db.Column(db.String, unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean(), default=True)
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    roles = db.relationship('Role', secondary='user_roles', backref=db.backref('users', lazy='dynamic'))
    
    def __repr__(self):
        return f'<User {self.email}>'


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    category = db.Column(db.String(10))  # Primary, Secondary, Tertiary
    name = db.Column(db.String(80), unique=True)  # role
    description = db.Column(db.String(255))

    def __repr__(self):
        return f"<Role {self.name}>"

class Notifications(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=func.now(), server_default=func.now(), nullable=False)

    def __repr__(self):
        return f'<Notification(title={self.title}, created_at={self.created_at})>'


class GitUser(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    userId = db.Column(db.Integer(), db.ForeignKey('user.id'))
    owner = db.Column(db.String(255))
    token = db.Column(db.String(255))

class Projects(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(25), nullable=False, unique=True)
    description = db.Column(db.String(255))

    def __repr__(self):
        return f"<Projects {self.title}>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description
        }
    
class Milestones(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id') ,nullable = False)
    task_no = db.Column(db.Integer, nullable=False)
    task = db.Column(db.String(25), nullable=False)
    description = db.Column(db.String(255))
    deadline = db.Column(db.TIMESTAMP)  # deadline=datetime(2024, 11, 15, 14, 30, 0) -> YYYY, MM, DD, HH, MM, SS
    

# class Teams(db.Model):
#     id = db.Column(db.Integer(), primary_key=True)
#     project_id = db.Column(db.Integer, db.ForeignKey('projects.id') ,nullable = False)
#     name = db.Column(db.String(20), nullable=False, unique=True)

# class MilestoneTracker(db.Model):
#     id = db.Column(db.Integer(), primary_key=True)
#     team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))
#     project_id = db.Column(db.Integer, db.ForeignKey('projects.id') ,nullable = False)
#     name = db.Column(db.String(20), nullable=False, unique=True) 