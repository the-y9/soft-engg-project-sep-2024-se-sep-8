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
    email = db.Column(db.String, unique=True, index=True)
    username = db.Column(db.String, unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean(), default=True)
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    roles = db.relationship('Role', secondary='user_roles', backref=db.backref('users', lazy='dynamic'))
    
    def __repr__(self):
        return f'<User {self.email}>'


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    category = db.Column(db.String(10), db.CheckConstraint("category IN ('Primary', 'Secondary', 'Tertiary')"), nullable=False)
    name = db.Column(db.String(80), unique=True)  # role
    description = db.Column(db.String(255))

    def __repr__(self):
        return f"<Role {self.name}>"

class Notifications(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_for = db.Column(db.Integer, db.ForeignKey('team.id'))
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=func.now(), server_default=func.now(), nullable=False)

    def __repr__(self):
        return f'<Notification(title={self.title}, created_at={self.created_at})>'

class NotificationUser(db.Model):
    __tablename__ = 'notification_user'
    
    notification_id = db.Column(db.Integer, db.ForeignKey('notifications.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)

    notification = db.relationship('Notifications', backref=db.backref('users', lazy='dynamic'))
    user = db.relationship('User', backref=db.backref('notifications', lazy='dynamic'))

    def __repr__(self):
        return f'<NotificationUser(notification_id={self.notification_id}, user_id={self.user_id})>'


class GitUser(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    userId = db.Column(db.Integer(), db.ForeignKey('user.id'))
    owner = db.Column(db.String(255))
    token = db.Column(db.String(255))

class Projects(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(25), nullable=False, unique=True)
    description = db.Column(db.String(255))
    start_date = db.Column(db.TIMESTAMP)
    end_date = db.Column(db.TIMESTAMP)

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
    

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.String(255))
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    members = db.relationship('User', secondary='team_members', backref=db.backref('teams', lazy='dynamic'))
    notifications = db.relationship('Notifications', backref='team', lazy='dynamic')  # Relationship to Notifications
    repo_owner = db.Column(db.Integer, db.ForeignKey('git_user.id'))
    repo_name = db.Column(db.String(100))

    def __repr__(self):
        return f'<Team {self.name}>'

class TeamMembers(db.Model):
    __tablename__ = 'team_members'
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class MilestoneTracker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    milestone_id = db.Column(db.Integer, db.ForeignKey('milestones.id'), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    progress = db.Column(db.Float, default=0.0)  # Percentage of progress
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    
    def __repr__(self):
        return f'<MilestoneTracker(milestone_id={self.milestone_id}, progress={self.progress})>'

class FileStorage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    file_url = db.Column(db.String(255), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=func.now(), nullable=False)
    uploaded_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    related_milestone = db.Column(db.Integer, db.ForeignKey('milestones.id'))
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    
    def __repr__(self):
        return f'<FileStorage(filename={self.filename}, uploaded_by={self.uploaded_by})>'


class EvaluationCriteria(db.Model):
    __tablename__ = 'evaluation_criteria'
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    criterion = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)

class PeerReview(db.Model):
    __tablename__ = 'peer_reviews'
    id = db.Column(db.Integer, primary_key=True)
    reviewer_id = db.Column(db.Integer, nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    criteria = db.Column(db.JSON, nullable=False)  # Stores a JSON array of criteria evaluations
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

class SystemLog(db.Model):
    __tablename__ = 'system_logs'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    severity = db.Column(db.String(20), nullable=False)  # e.g., INFO, WARNING, ERROR
    message = db.Column(db.Text, nullable=False)
