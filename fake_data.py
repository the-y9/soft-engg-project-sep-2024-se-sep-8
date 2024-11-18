from main import app
from backend.security import datastore 
from backend.models import db, Role, GitUser, Projects, Milestones, Notifications
from werkzeug.security import generate_password_hash
from datetime import datetime


from main import app
from backend.security import datastore 
from backend.models import db, Role, GitUser, Projects, Milestones, Notifications
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
from faker import Faker
import random

fake = Faker()

with app.app_context():
    db.create_all()
    # Define role data
    roles_data = [
        {"category": "Primary", "name": "instructor", "description": "User who teaches and manages projects"},
        {"category": "Primary", "name": "student", "description": "User who works on projects"},
        {"category": "Secondary", "name": "admin", "description": "User who manages the system"},
        {"category": "Secondary", "name": "ta", "description": "User who assists instructors"},
        {"category": "Tertiary", "name": "extEval", "description": "User who evaluates"}
    ]
    
    # Create roles
    for role in roles_data:
        datastore.find_or_create_role(
            category=role["category"],
            name=role["name"],
            description=role["description"]
        )   
    print(f"{len(roles_data)} roles created.")

    db.session.commit()

    # Define user data
    users_data = [
        {"email": "admin@g.com", "password": "admin", "roles": ["admin"]},
        {"email": "ins@g.com","username":"ins", "password": "ins", "roles": ["instructor"]},
        {"email": "stud@g.com", "password": "stud", "roles": ["student"]},
        {"email": "ta@g.com", "password": "ta", "roles": ["ta"]},
        {"email": "ee@g.com", "password": "ee", "roles": ["extEval"]},
        {"email": "rough@g.com", "password": "rough", "roles": ["student"]}
    ]

    # Create users
    try:
        for user in users_data:
            if not datastore.find_user(email=user["email"]):
                datastore.create_user(
                    email=user["email"],
                    username = user.get("username", user["email"]),
                    password=generate_password_hash(user["password"]),
                    roles=user["roles"]
                )
        print(f"{len(users_data)} users created.")
        db.session.commit()
    
    except Exception as e:
        print(f"ERROR: {e}")



    # Add 100 random users to the database
    try:
        for _ in range(100):
            email = fake.unique.email()
            username = fake.user_name()
            password = generate_password_hash("password")
            roles = random.choices(["admin", "student", "instructor", "ta", "extEval"], k=random.randint(1, 2))
            
            if not datastore.find_user(email=email):
                datastore.create_user(
                    email=email,
                    username=username,
                    password=password,
                    roles=roles
                )
        print("100 random users created.")
        db.session.commit()
    except Exception as e:
        print(f"ERROR (Users): {e}")

    # Add 100 random GitUser entries
    try:
        user_ids = [user.id for user in datastore.user_model.query.all()]
        for _ in range(100):
            git_user = GitUser(
                userId=random.choice(user_ids),
                owner=fake.user_name(),
                token=fake.sha256()
            )
            db.session.add(git_user)
        db.session.commit()
        print("100 random GitUsers created.")
    except Exception as e:
        print(f"ERROR (GitUser): {e}")

    # Add 100 random projects
    try:
        for _ in range(100):
            project = Projects(
                title=fake.catch_phrase(),
                description=fake.text(max_nb_chars=200)
            )
            db.session.add(project)
        db.session.commit()
        print("100 random projects created.")
    except Exception as e:
        print(f"ERROR (Projects): {e}")

    # Add 100 random milestones
    try:
        project_ids = [project.id for project in Projects.query.all()]
        for _ in range(500):
            milestone = Milestones(
                project_id=random.choice(project_ids),
                task_no=random.randint(1, 5),
                task=fake.bs().capitalize(),
                description=fake.text(max_nb_chars=150),
                deadline=datetime.now() + timedelta(days=random.randint(1, 365))
            )
            db.session.add(milestone)
        db.session.commit()
        print("500 random milestones created.")
    except Exception as e:
        print(f"ERROR (Milestones): {e}")

    # Add 100 random notifications
    try:
        user_ids = [user.id for user in datastore.user_model.query.all()]
        for _ in range(100):
            notification = Notifications(
                title=fake.sentence(nb_words=6),
                message=fake.paragraph(nb_sentences=3),
                created_for=random.choice(user_ids) if user_ids else None,
                created_by=random.choice(user_ids),
                created_at=datetime.now()
            )
            db.session.add(notification)
        db.session.commit()
        print("100 random notifications created.")
    except Exception as e:
        print(f"ERROR (Notifications): {e}")
