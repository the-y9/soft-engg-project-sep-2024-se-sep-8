from flask_restful import Resource, Api, reqparse, marshal_with, fields
from flask_security import auth_required, roles_required, current_user
from backend.models import db
from sqlalchemy import func
from flask import jsonify, request
from .instance import cache
from .models import User, GitUser, Projects, Milestones, Notifications, Team, TeamMembers
import requests
from datetime import datetime
from .other_api import other_api_bp
import google.generativeai as genai
import pandas as pd
import json
import re
GOOGLE_API_KEY = 'AIzaSyBXWPw2U4D1DuOtEDRLrCBcNxnb1qlBh30'
genai.configure(api_key=GOOGLE_API_KEY)


api = Api()

def key(owner):
    try:
        git_user = GitUser.query.filter_by(owner = owner).first()
        if git_user:
            return git_user.token
        return "Git Error"
    except Exception as e:
        return jsonify({"message":f"Error: {e}"})


class GitHubRepo(Resource):
    def check_owner_exists(self, owner):
        """Checks if a user exists on GitHub using the GitHub API."""
        url = f"https://api.github.com/users/{owner}"
        response = requests.get(url)
        return response.status_code == 200

    def get(self, owner, repo=None):
        # token=key("rough@g.com")
        """Handles both checking if the owner exists and getting repository commits."""
        
        if not self.check_owner_exists(owner):
            return jsonify({"message": f"Owner '{owner}' not found on GitHub."})

        if not repo:
            return jsonify({"message": f"'{owner}' is a valid owner name."})

        try:
            # Fetch commit information for the repository
            url = f"https://api.github.com/repos/{owner}/{repo}/commits"
            token = ""
            token = key(owner)
            headers = {}
            if token:
                headers['Authorization'] = f'token {token}'
                headers['Accept'] = "application/vnd.github.v3+json"
            
            response = requests.get(url)
            if response.status_code == 200:
                commits = response.json()
                commit_data = [{
                    'sha': commit['sha'],
                    'message': commit['commit']['message'],
                    'committer_name': commit['commit']['committer']['name'],  # Who applied the commit
                    'commit_date': commit['commit']['committer']['date'],
                    'author_name': commit['commit']['author']['name'],  # Who originally wrote the commit
                    'author_date': commit['commit']['author']['date']
                } for commit in commits]
                return jsonify({"total_commits":len(commit_data),"commit_data":commit_data})
            elif response.status_code == 404:
                return jsonify({"message": f"Error: Repository '{repo}' not found!"})
            else:
                return jsonify({"message":f"Error: {response.status_code}"})
        except Exception as e:
            return jsonify({"message":f"Error: {e}"})

# Add the resource with different routes for owner and repo
api.add_resource(GitHubRepo, '/owner/<string:owner>', '/owner/<string:owner>/repo/<string:repo>/commits')

class Project_Manager(Resource):
    
    # Get a specific milestone by ID
    def get(self, id=None,project_id=None):
        if id:
            try:
                milestone = Milestones.query.get(id)
                if milestone:
                    return jsonify({
                        'id': milestone.id,
                        'project_id': milestone.project_id,
                        'task_no': milestone.task_no,
                        'task': milestone.task,
                        'description': milestone.description,
                        'deadline': milestone.deadline
                    })
                return jsonify({'message': 'Milestone not found'})
            except Exception as e:
                return jsonify({'ERROR': f'{e}'})

    # Get all milestones for a specific project
    
        elif project_id:
            project = Projects.query.filter_by(id=project_id).first()
            milestones = Milestones.query.filter_by(project_id=project_id).all()
            if milestones:
                return jsonify({
                    'id': project.id,
                    'name': project.title,
                    'description': project.description,
                    'startDate': project.start_date.strftime('%Y-%m-%d') if project.start_date else None,
                    'endDate': project.end_date.strftime('%Y-%m-%d') if project.end_date else None,
                    'milestones':
                    [{
                    'id': milestone.id,
                    'task_no': milestone.task_no,
                    'taskName': milestone.task,
                    'description': milestone.description,
                    'deadline': milestone.deadline
                } for milestone in milestones]})
            return jsonify({'message': 'Milestones not found for the project'})
        

        '''{
                id: 2,
                name: 'Project Beta',
                teams: [{ id: 3, name: 'Team C' }],
                startDate: '2024-03-01',
                endDate: '2024-08-15',
                milestones: [
                    { id: 201, name: 'Milestone 1', status: 'Pending' }
                ]
            }
        '''
        # Case 2: Get all projects
        all_projects = Projects.query.all()  # Retrieve all projects from the database

        if all_projects:
            result = []
            
            for project in all_projects:
                # Get teams related to the project
                teams = [
                    {'id': team.id, 'name': team.name, 'repo_owner': team.repo_owner, 'repo_name': team.repo_name} for team in Team.query.filter_by(project_id=project.id).all()
                ]
                
                # Get milestones related to the project
                milestones = [
                    {'id': milestone.id, 'name': milestone.task, 'status': 'Pending'} for milestone in Milestones.query.filter_by(project_id=project.id).all()
                ]
                
                # Add project data to the result list
                result.append({
                    'id': project.id,
                    'name': project.title,
                    'teams': teams,
                    'startDate': project.start_date.strftime('%Y-%m-%d') if project.start_date else None,
                    'endDate': project.end_date.strftime('%Y-%m-%d') if project.end_date else None,
                    'milestones': milestones
                })
            
            # print(result[0])
            return jsonify(result)

        # Return message if no projects found
        return jsonify({'message': 'No projects found'})

    # Create a new
    @roles_required('instructor')
    def post(self):
        data = request.get_json()

        if 'title' in data:
            # Check if the project already exists
            existing_project = Projects.query.filter_by(title=data['title']).first()
            if existing_project:
                return jsonify({'message': 'Project with this title already exists'}), 400

            # Create a new project
            new_project = Projects(
                title=data['title'],
                description=data.get('description', ''),  # Default to empty string if description is not provided
                start_date = datetime.strptime(data['start_date'], '%Y-%m-%d') if 'start_date' in data else None,
                end_date = datetime.strptime(data['end_date'], '%Y-%m-%d') if 'end_date' in data else None
            )
            db.session.add(new_project)
            db.session.commit()

            return {
                'id': new_project.id,
                'title': new_project.title,
                'description': new_project.description,
                'start_date' : new_project.start_date.strftime('%Y-%m-%d %H:%M:%S') if new_project.start_date else None,
                'end_date' : new_project.end_date.strftime('%Y-%m-%d %H:%M:%S') if new_project.end_date else None
            }

        # Case 2: Create a new milestone
        elif 'project_id' in data and 'milestones' in data:
            project = Projects.query.get(data['project_id'])
            if not project:
                return jsonify({'message': 'Project not found'}), 404
            milestones = data["milestones"]
            new_milestones = []
            for index, milestone in enumerate(milestones):
                new_milestone = Milestones(
                    project_id=data['project_id'],
                    task_no=index+1,
                    task=milestone['task'],
                    description=milestone.get('description', ''),
                    deadline=datetime.strptime(milestone['deadline'], '%Y-%m-%d') if 'deadline' in milestone else None
                )
                db.session.add(new_milestone)
                new_milestones.append(new_milestone)

            db.session.commit()

            serialized_milestones = [
                        {
                            'task_no': m.task_no,
                            'task': m.task,
                            'description': m.description,
                            'deadline': m.deadline.strftime('%Y-%m-%d %H:%M:%S') if m.deadline else None
                        }
                        for m in new_milestones
            ]
            return {
                'project_id': project.id,
                'milestones': serialized_milestones
            }

        # Case 3: Invalid request (missing required fields)
        return jsonify({'message': 'Invalid data for creating project or milestone'})


    # Delete a milestone
    @roles_required('instructor')
    def delete(self, id=None,project_id=None):
        if id:
            milestone = Milestones.query.get(id)
            if not milestone:
                return jsonify({'message': 'Milestone not found'})

            db.session.delete(milestone)
            db.session.commit()
            return jsonify({'message': 'Milestone deleted successfully'})
        # return {'message': 'ID is required to delete a milestone'}, 400
    
    # Delete a project
    
        if project_id:
            project = Projects.query.filter_by(id=project_id).first()
            
            if not project:
                return jsonify({'message': 'project not found'})

            db.session.delete(project)
            db.session.commit()
            return jsonify({'message': 'project deleted successfully'})
        return {'message': 'ID is required to delete. '}

    @roles_required('instructor')
    def put(self, id=None):
        data = request.get_json()

        # Update a milestone
        if id:
            milestone = Milestones.query.get(id)
            if not milestone:
                return jsonify({'message': 'Milestone not found'})

            # Update milestone fields
            milestone.task_no = data.get('task_no', milestone.task_no)
            milestone.task = data.get('task', milestone.task)
            milestone.description = data.get('description', milestone.description)
            if 'deadline' in data:
                try:
                    milestone.deadline = datetime.strptime(data['deadline'], '%Y-%m-%d %H:%M:%S')
                except ValueError:
                    return jsonify({'message': 'Invalid deadline format. Use YYYY-MM-DD HH:MM:SS'})

            db.session.commit()
            return jsonify({
                'id': milestone.id,
                'task_no': milestone.task_no,
                'task': milestone.task,
                'description': milestone.description,
                'deadline': milestone.deadline.strftime('%Y-%m-%d %H:%M:%S') if milestone.deadline else None
            })

        # Invalid request
        return jsonify({'message': 'Invalid request. Provide a milestone ID to update.'})

    # Update a specific project
    @roles_required('instructor')
    def put(self, project_id=None):
        data = request.get_json()

        # Update a project
        if project_id:
            project = Projects.query.get(project_id)
            if not project:
                return jsonify({'message': 'Project not found'})

            # Update project fields
            project.title = data.get('title', project.title)
            project.description = data.get('description', project.description)
            if 'start_date' in data:
                try:
                    project.start_date = datetime.strptime(data['start_date'], '%Y-%m-%d')
                except ValueError:
                    return jsonify({'message': 'Invalid start_date format. Use YYYY-MM-DD'})

            if 'end_date' in data:
                try:
                    project.end_date = datetime.strptime(data['end_date'], '%Y-%m-%d')
                except ValueError:
                    return jsonify({'message': 'Invalid end_date format. Use YYYY-MM-DD'})

            db.session.commit()
            return jsonify({
                'id': project.id,
                'title': project.title,
                'description': project.description,
                'start_date': project.start_date.strftime('%Y-%m-%d') if project.start_date else None,
                'end_date': project.end_date.strftime('%Y-%m-%d') if project.end_date else None
            })

        # Invalid request
        return jsonify({'message': 'Invalid request. Provide a project ID to update.'})
# Add resources to the API with different routes
api.add_resource(Project_Manager, '/projects','/project','/projects/<int:project_id>', '/milestone', '/milestone/<int:id>', '/project/<int:project_id>/milestones')

class Notification_Manager(Resource):
    # @roles_required('instructor')
    def get(self, id=None, user_id=None):
        if id:
            try:
                notification = Notifications.query.get(id)
                if notification:
                    return jsonify({
                        'id': notification.id,
                        'title': notification.title,
                        'message': notification.message,
                        'created_at': notification.created_at
                    }), 200
                return jsonify({'message': 'Notification not found'})
            except Exception as e:
                return jsonify({'ERROR': f'{e}'})
        
        elif user_id:
            notifications = Notifications.query.filter_by(created_for=user_id).all()
            
            if notifications:
                notification_list = [{
                    'id': notification.id,
                    'title': notification.title,
                    'message': notification.message
                } for notification in notifications]
                return notification_list, 200
            return jsonify({'message': 'No notifications found for this team'}), 404

        return {'message': 'Team ID or Notification ID is required'}, 400
    
    def post(self):
        data = request.get_json()

        # Ensure required fields are present
        if not all(key in data for key in ['notificationTitle', 'notificationMessage']):
            return jsonify({'message': 'Missing required fields'})

        try:
            if 'teamId' in data and data['teamId']:
                # Add notification for all team members
                team_members = TeamMembers.query.filter_by(team_id=data['teamId']).all() 
                if not team_members:
                    return jsonify({'message': 'No members found for the specified team.'})

                notifications = []
                for member in team_members:
                    notification = Notifications(
                        title=data['notificationTitle'],
                        message=data['notificationMessage'],
                        created_for=member.user_id,
                        created_by=data['instructorId']
                    )
                    db.session.add(notification)
                    notifications.append(notification)

                db.session.commit()

                notification_data = [
                    {
                        'id': notification.id,
                        'title': notification.title,
                        'message': notification.message,
                        'created_for': notification.created_for,
                        'created_by': notification.created_by,
                        'created_at': notification.created_at
                    }
                    for notification in notifications
                ]

                return jsonify({'message': 'Notifications created successfully for all team members.', 'data': notification_data})

            elif 'memberId' in data and data['memberId']:
                # Add notification for a specific member
                new_notification = Notifications(
                    title=data['notificationTitle'],
                    message=data['notificationMessage'],
                    created_for=data['memberId'],  # No team ID if it's specific to a member
                    created_by=data['instructorId']
                )
                db.session.add(new_notification)
                db.session.commit()

                notification_data = {
                    'id': new_notification.id,
                    'title': new_notification.title,
                    'message': new_notification.message,
                    'created_for': new_notification.created_for,
                    'created_by': new_notification.created_by,
                    'created_at': new_notification.created_at
                }

                return jsonify({'message': 'Notification created successfully for the member.', 'data': notification_data})

            else:
                return jsonify({'message': 'Either teamId or memberId must be provided.'})

        except Exception as e:
            return jsonify({'ERROR': f'{e}'})
        
    @roles_required('instructor')
    def delete(self, id=None):
        if id:
            notification = Notifications.query.get(id)
            if not notification:
                return jsonify({'message': 'Notification not found'}), 404

            db.session.delete(notification)
            db.session.commit()
            return jsonify({'message': 'Notification deleted successfully'}), 200

        return jsonify({'message': 'Notification ID is required to delete a notification'}), 404

api.add_resource(
    Notification_Manager,
    '/notifications',  # For creating a new notification (POST)
    '/notifications/<int:id>',  # For fetching or deleting a specific notification by ID (GET/DELETE)
    '/notifications/user/<int:user_id>'  # For fetching all notifications for a specific user (GET)
)

class ProjectUpdate(Resource):
    # Update a specific project
    @roles_required('instructor')
    def put(self, project_id=None):
        data = request.get_json()

        # Update a project
        if project_id:
            project = Projects.query.get(project_id)
            if not project:
                return jsonify({'message': 'Project not found'}), 404

            # Update project fields
            project.title = data.get('name', project.title)
            project.description = data.get('description', project.description)
            if 'startDate' in data:
                try:
                    project.start_date = datetime.strptime(data['startDate'], '%Y-%m-%d')
                except ValueError:
                    return jsonify({'message': 'Invalid start_date format. Use YYYY-MM-DD'}), 400

            if 'endDate' in data:
                try:
                    project.end_date = datetime.strptime(data['endDate'], '%Y-%m-%d')
                except ValueError:
                    return jsonify({'message': 'Invalid end_date format. Use YYYY-MM-DD'}), 400

            db.session.commit()
            return {
                'id': project.id,
                'name': project.title,
                'description': project.description,
                'start_date': project.start_date.strftime('%Y-%m-%d') if project.start_date else None,
                'end_date': project.end_date.strftime('%Y-%m-%d') if project.end_date else None
            }, 200

        # Invalid request
        return jsonify({'message': 'Invalid request. Provide a project ID to update.'}), 400
    
api.add_resource(ProjectUpdate,'/projects/update/<int:project_id>')


import random
from datetime import datetime, timedelta

class StudPerfom(Resource):
    def post(self):
        data = request.get_json()

        if 'repoOwner' not in data or 'repoName' not in data or 'teamId' not in data:
            return {'message': 'Missing repoOwner, repoName, or teamId'}

        repo_owner = data['repoOwner']
        repo_name = data['repoName']
        team_id = data['teamId']

        # Fetch team and commit data (simulate or fetch from database)
        team = Team.query.filter_by(id=team_id).first()
        if not team:
            return jsonify({"message": f"Team with id {team_id} not found."})

        def generate_mock_commits(team_members, num_commits=10):
            """Generate synthetic commit history."""
            mock_commits = []
            for _ in range(num_commits):
                member = random.choice(team_members)
                commit_date = datetime.now() - timedelta(days=random.randint(1, 90))
                mock_commits.append({
                    "sha": f"mock-{random.randint(1000, 9999)}",
                    "commit_date": commit_date.isoformat(),
                    "author": member.username,
                    "message": f"Mock commit by {member.username} on {repo_name}"
                })
            return mock_commits

        team_members = team.members
        # if not team_members:
        #     return jsonify({"message": "No team members found."})

        github_repo = GitHubRepo()
        try:
            if not github_repo.check_owner_exists(repo_owner):
                raise Exception("GitHub owner not found.")
            commit_response = github_repo.get(repo_owner, repo_name)
            commits = commit_response.get_json().get('commit_data', [])
        except Exception:
            commits = []

        if not commits:
            commits = generate_mock_commits(team_members)

        if commits:
            prompt = f"""
            Analyze the commit history of a GitHub repository to evaluate team members' performance.
            Repository Owner: {repo_owner}
            Repository Name: {repo_name}
            Commits:
            {json.dumps(commits, indent=4)}

            Output requirements:
            - Provide a JSON-formatted report of each team member's performance
            - Include fields: 'name', 'contributionScore', 'details'
            - Assess the quality and frequency of commits

            Example Output:
            [
                {{
                    "name": "John Doe",
                    "contributionScore": 85,
                    "details": "Consistent and meaningful commits."
                }},
                {{
                    "name": "Jane Smith",
                    "contributionScore": 70,
                    "details": "Frequent commits but requires more depth."
                }}
            ]
            """
        else:
            prompt = """
            The provided commit history is empty, so no data is available for analysis.
            Generate a JSON-formatted placeholder report for team members, noting the absence of activity.

            Example Output:
            [
                {
                    "name": "John Doe",
                    "contributionScore": 0,
                    "details": "No commits found in the provided history."
                },
                {
                    "name": "Jane Smith",
                    "contributionScore": 0,
                    "details": "No commits found in the provided history."
                }
            ]
            """

        try:
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(prompt)
            ai_output = response.text.strip()

            json_match = re.search(r'\[\s*{.*?}\s*(?:,\s*{.*?}\s*)*\]', ai_output, re.DOTALL)

            if not json_match:
                return {
                    'ERROR': 'Could not extract JSON content',
                    'raw_output': ai_output
                }

            try:
                performance_report = json.loads(json_match.group(0))

                if not isinstance(performance_report, list):
                    raise ValueError("Extracted content is not a list of performance reports")

                for member in performance_report:
                    if not all(key in member for key in ['name', 'contributionScore', 'details']):
                        raise ValueError("Performance report is missing required fields")

                return {'performanceReport': performance_report}

            except (json.JSONDecodeError, ValueError) as e:
                return {
                    'ERROR': f'Invalid performance report format: {str(e)}',
                    'raw_output': ai_output
                }

        except Exception as e:
            return {
                'ERROR': f'Failed to evaluate performance: {str(e)}'
            }
api.add_resource(StudPerfom, '/evaluate-performance')
