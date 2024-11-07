from main import app
from backend.security import datastore 
from backend.models import db, Role, GitUser
from werkzeug.security import generate_password_hash

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
        existing_role = datastore.find_or_create_role(
            category=role["category"],
            name=role["name"],
            description=role["description"]
        )
        if existing_role:
            print(f"Role '{existing_role.name}' created with category '{existing_role.category}'.")

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
        print(f"{len(users_data)} roles created.")
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