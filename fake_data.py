from main import app
from backend.security import datastore
from backend.models import db, Role, GitUser, Projects, Milestones, Notifications, User, Team, FileStorage, EvaluationCriteria, PeerReview, SystemLog, MilestoneTracker, NotificationUser, TeamMembers,RolesUsers
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
from faker import Faker
import random
import string
from sqlalchemy.exc import IntegrityError

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
        {"email": "ins@g.com", "username":"ins", "password": "ins", "roles": ["instructor"]},
        {"email": "stud@g.com", "username":"stud", "password": "stud", "roles": ["student"]},
        {"email": "ta@g.com", "username":"ta", "password": "ta", "roles": ["ta"]},
        {"email": "ee@g.com", "username":"ee", "password": "ee", "roles": ["extEval"]},
        {"email": "rough@g.com","username":"rough", "password": "rough", "roles": ["student"]}
    ]

    # Create users
    try:
        for user in users_data:
            if not datastore.find_user(email=user["email"]):
                datastore.create_user(
                    email=user["email"],
                    username=user.get("username", user["email"]),
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

    # Add 10 random projects with start and end dates
    try:
        for _ in range(10):
            project = Projects(
                title=fake.catch_phrase(),
                description=fake.text(max_nb_chars=200),
                start_date=fake.date_this_decade(),
                end_date=fake.date_this_decade()
            )
            db.session.add(project)
        db.session.commit()
        print("10 random projects created.")
    except Exception as e:
        print(f"ERROR (Projects): {e}")

    # Add 50 random milestones
    try:
        project_ids = [project.id for project in Projects.query.all()]
        for _ in range(50):
            milestone = Milestones(
                project_id=random.choice(project_ids),
                task_no=random.randint(1, 5),
                task=fake.bs().capitalize(),
                description=fake.text(max_nb_chars=150),
                deadline=datetime.now() + timedelta(days=random.randint(1, 365))
            )
            db.session.add(milestone)
        db.session.commit()
        print("50 random milestones created.")
    except Exception as e:
        print(f"ERROR (Milestones): {e}")

    # Helper function to generate unique team names
    def generate_unique_team_name(existing_names):
        while True:
            random_suffix = ''.join(random.choices(string.ascii_letters + string.digits, k=5))
            team_name = f"Team-{random_suffix}"
            if team_name not in existing_names:
                existing_names.add(team_name)
                return team_name

    # Create 100 random teams with valid `repo_owner` and `team_members`
    existing_team_names = set()

    try:
        for _ in range(100):
            # Generate a unique team name
            team_name = generate_unique_team_name(existing_team_names)
            description = "Random team description"
            
            # Ensure repo_owner is a valid string representing the owner (could be a GitHub username or another identifier)
            repo_owner = fake.user_name()  # This could be any string representing the repository owner

            # Create the team with a valid `repo_owner`
            team = Team(
                name=team_name,
                description=description,
                project_id=random.choice([project.id for project in Projects.query.all()]),
                repo_owner=repo_owner,  # Set the repo_owner to a string (GitHub username, for example)
                repo_name=''.join(random.choices(string.ascii_lowercase, k=8))  # Random repo name
            )
            
            db.session.add(team)
            db.session.commit()

            # Create the team_members entry for the `repo_owner` (the user who is the repo owner must be added as a team member)
            team_member = TeamMembers(
                team_id=team.id,  # This associates the user with the created team
                user_id=random.choice([user.id for user in User.query.all()])  # Random user ID from the User table
            )
            db.session.add(team_member)

            # Now, we can add additional team members if needed (not necessarily the `repo_owner`)
            for _ in range(random.randint(1, 5)):  # Add 1 to 5 other random team members
                random_user = random.choice([user for user in User.query.all() if user.id != team_member.user_id])
                team_member = TeamMembers(
                    team_id=team.id,
                    user_id=random_user.id
                )
                db.session.add(team_member)
            
            db.session.commit()
        
        print("100 random teams with team members created successfully.")
    except Exception as e:
        print(f"ERROR (Teams & TeamMembers): {e}")
        db.session.rollback()




    # Add 100 random file storage entries
    try:
        for _ in range(100):
            file_storage = FileStorage(
                filename=fake.file_name(),
                file_url=fake.url(),
                uploaded_by=random.choice([user.id for user in User.query.all()]),
                team_id=random.choice([team.id for team in Team.query.all()]),
                related_milestone=random.choice([milestone.id for milestone in Milestones.query.all()]) if Milestones.query.all() else None
            )
            db.session.add(file_storage)
        db.session.commit()
        print("100 random file storage entries created.")
    except Exception as e:
        print(f"ERROR (FileStorage) at {_}: {e}")

    # Add 100 random evaluation criteria entries
    try:
        for _ in range(100):
            evaluation_criteria = EvaluationCriteria(
                project_id=random.choice([project.id for project in Projects.query.all()]),
                criterion=fake.sentence(),
                description=fake.text()
            )
            db.session.add(evaluation_criteria)
        db.session.commit()
        print("100 random evaluation criteria entries created.")
    except Exception as e:
        print(f"ERROR (EvaluationCriteria): {e}")

    # Add 100 random peer reviews
    try:
        for _ in range(100):
            peer_review = PeerReview(
                reviewer_id=random.choice([user.id for user in User.query.all()]),
                project_id=random.choice([project.id for project in Projects.query.all()]),
                criteria=[{"criterion": fake.sentence(), "score": random.randint(1, 5)}],
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            db.session.add(peer_review)
        db.session.commit()
        print("100 random peer reviews created.")
    except Exception as e:
        print(f"ERROR (PeerReview): {e}")

    # Add 100 random system log entries
    try:
        for _ in range(100):
            system_log = SystemLog(
                severity=random.choice(["INFO", "WARNING", "ERROR"]),
                message=fake.text()
            )
            db.session.add(system_log)
        db.session.commit()
        print("100 random system logs created.")
    except Exception as e:
        print(f"ERROR (SystemLog): {e}")

    # Add 100 random milestone trackers
    try:
        milestone_ids = [milestone.id for milestone in Milestones.query.all()]
        team_ids = [team.id for team in Team.query.all()]
        for _ in range(100):
            milestone_tracker = MilestoneTracker(
                milestone_id=random.choice(milestone_ids),
                team_id=random.choice(team_ids),
                progress=random.uniform(0, 100),
                updated_at=datetime.now()
            )
            db.session.add(milestone_tracker)
        db.session.commit()
        print("100 random milestone trackers created.")
    except Exception as e:
        print(f"ERROR (MilestoneTracker): {e}")

    # Add random team members
    try:
        team_ids = [team.id for team in Team.query.all()]
        user_ids = [user.id for user in User.query.all()]
        for _ in range(100):
            team_member = TeamMembers(
                team_id=random.choice(team_ids),
                user_id=random.choice(user_ids)
            )
            db.session.add(team_member)
        db.session.commit()
        print("100 random team members created.")
    except Exception as e:
        print(f"ERROR (TeamMembers): {e}")


    try:
        user_ids = [user.id for user in User.query.join(RolesUsers).join(Role)
    .filter(Role.name == 'instructor')
    .all()]
        team_ids = [team.id for team in Team.query.all()]

        for _ in range(100):
            notification = Notifications(
                title=fake.sentence(),
                message=fake.text(),  # Random message
                # created_for=random.choice(team_ids),
                created_by=random.choice(user_ids),
                created_at=datetime.now()  # Current timestamp
            )
            db.session.add(notification)

        db.session.commit()
        print("100  notifications created successfully")

    except Exception as e:
        db.session.rollback()  # Ensure rollback in case of error
        print(f"ERROR (Notifications): {str(e)}")


    # Add 100 random notification users
    try:
        user_ids = [user.id for user in User.query.all()]
        for _ in range(100):
            notification_user = NotificationUser(
                notification_id=random.choice([notification.id for notification in Notifications.query.all()]),
                user_id=random.choice(user_ids)
            )
            db.session.add(notification_user)
        db.session.commit()
        print("100 random notification users created.")
    except Exception as e:
        print(f"ERROR (NotificationUser): {e}")
