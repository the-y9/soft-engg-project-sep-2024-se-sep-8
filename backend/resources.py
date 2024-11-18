from flask_restful import Resource, Api, reqparse, marshal_with, fields
from flask_security import auth_required, roles_required, current_user
from backend.models import db
from sqlalchemy import func
from flask import jsonify, request
from .instance import cache
from .models import User, GitUser, Projects, Milestones
import requests
from datetime import datetime


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
            # token = "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"
            token = key(owner)
            headers = {}
            if token:
                headers['Authorization'] = f'token {token}'
                headers['Accept'] = "application/vnd.github.v3+json"
            
            response = requests.get(url,headers=headers)
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

        else:
            return jsonify({"message": f"Error retrieving commits: {response.status_code}"}), response.status_code

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
                return jsonify({'ERROR': f'{e}'}), 400

    # Get all milestones for a specific project
    
        elif project_id:
            project = Projects.query.filter_by(id=project_id).first()
            milestones = Milestones.query.filter_by(project_id=project_id).all()
            print(project)
            if milestones:
                return jsonify({
                    'project' : project.to_dict(),
                    'milestones':
                    [{
                    'id': milestone.id,
                    'task_no': milestone.task_no,
                    'task': milestone.task,
                    'description': milestone.description,
                    'deadline': milestone.deadline
                } for milestone in milestones]})
            return jsonify({'message': 'Milestones not found for the project'})
        
        return {'message': 'Project ID is required to retrieve milestones'}

    # Create a new
    def post(self):
        data = request.get_json()

        # Case 1: Create a new project
        if 'title' in data:
            if 'title' not in data:
                return jsonify({'message': 'Project title is required'})

            # Check if the project already exists
            existing_project = Projects.query.filter_by(title=data['title']).first()
            if existing_project:
                return jsonify({'message': 'Project with this title already exists'})

            # Create a new project
            new_project = Projects(
                title=data['title'],
                description=data.get('description', '')  # Default to empty string if description is not provided
            )
            db.session.add(new_project)
            db.session.commit()

            return jsonify({
                'id': new_project.id,
                'title': new_project.title,
                'description': new_project.description
            })

        # Case 2: Create a new milestone
        elif 'project_id' in data and 'task_no' in data and 'task' in data:
            project = Projects.query.get(data['project_id'])
            if not project:
                return jsonify({'message': 'Project not found'})

            new_milestone = Milestones(
                project_id=data['project_id'],
                task_no=data['task_no'],
                task=data['task'],
                description=data.get('description', ''),
                deadline=datetime.strptime(data['deadline'], '%Y-%m-%d %H:%M:%S') if 'deadline' in data else None
            )
            db.session.add(new_milestone)
            db.session.commit()

            return jsonify({
                'id': new_milestone.id,
                'task_no': new_milestone.task_no,
                'task': new_milestone.task,
                'description': new_milestone.description,
                'deadline': new_milestone.deadline.strftime('%Y-%m-%d %H:%M:%S') if new_milestone.deadline else None
            }), 201

        # Case 3: Invalid request (missing required fields)
        return jsonify({'message': 'Invalid data for creating project or milestone'})


    # Delete a milestone
    def delete(self, id=None):
        if id:
            milestone = Milestones.query.get(id)
            if not milestone:
                return jsonify({'message': 'Milestone not found'}), 404

            db.session.delete(milestone)
            db.session.commit()
            return jsonify({'message': 'Milestone deleted successfully'}), 200
        return {'message': 'ID is required to delete a milestone'}, 400

# Add resources to the API with different routes
api.add_resource(Project_Manager, '/project', '/milestone', '/milestone/<int:id>', '/project/<int:project_id>/milestones')

