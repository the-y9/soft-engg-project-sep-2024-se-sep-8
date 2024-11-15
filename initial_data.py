from main import app
from backend.security import datastore 
from backend.models import db, Role, GitUser, Projects, Milestones
from werkzeug.security import generate_password_hash
from datetime import datetime

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


    # GitUser data
    gitUser = [
        {"userId": "6", "owner":"the-y9", "token": "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"}
    ]
    for user in gitUser:
        db.session.add( GitUser(
                userId=user['userId'],
                owner=user['owner'],
                token=user['token']
            ) )
    db.session.commit()

    # Projects and Milsestone data
    projects_data = [
    {"title": "Project Alpha", "description": "Description for Project Alpha."},
    {"title": "Project Beta", "description": "Description for Project Beta."},
    {"title": "Project Gamma", "description": "Description for Project Gamma."}
    ]

    milestones_data = [
    {"project_id": 1, "task_no": 1, "task": "Initial Planning", "description": "Complete the initial project planning.", "deadline": "2024-11-30 10:00:00"},
    {"project_id": 1, "task_no": 2, "task": "Design Phase", "description": "Begin designing the project structure.", "deadline": "2024-12-10 12:00:00"},
    {"project_id": 2, "task_no": 1, "task": "Requirement Gathering", "description": "Gather requirements for the project.", "deadline": "2024-12-01 09:00:00"},
    {"project_id": 2, "task_no": 2, "task": "Development Start", "description": "Begin the development phase.", "deadline": "2024-12-20 14:00:00"},
    {"project_id": 3, "task_no": 1, "task": "Market Research", "description": "Conduct market research for the new product.", "deadline": "2024-12-05 11:00:00"}
    ]

    try:
        for project_data in projects_data:
                project = Projects(
                    title=project_data["title"],
                    description=project_data["description"]
                )
                db.session.add(project)
        db.session.commit()

        for milestone_data in milestones_data:
                milestone = Milestones(
                    project_id=milestone_data["project_id"],
                    task_no=milestone_data["task_no"],
                    task=milestone_data["task"],
                    description=milestone_data["description"],
                    deadline=datetime.strptime(milestone_data["deadline"], "%Y-%m-%d %H:%M:%S")
                )
                db.session.add(milestone)
        db.session.commit()
        print("Dummy Project data inserted.")
    except Exception as e:
         print(f"ERROR: {e}")