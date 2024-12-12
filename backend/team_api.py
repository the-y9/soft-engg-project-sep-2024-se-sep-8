from flask import Blueprint, jsonify
from sqlalchemy.orm import joinedload
from .models import Projects, Team, Milestones, MilestoneTracker, GitUser, FileStorage, db, TeamMembers
from flask_restful import Resource, Api,request
from datetime import datetime
import requests
from .resources import GitHubRepo
from werkzeug.utils import secure_filename
import google.generativeai as genai
import pandas as pd
import json
import re
from werkzeug.utils import secure_filename
GOOGLE_API_KEY = 'AIzaSyBXWPw2U4D1DuOtEDRLrCBcNxnb1qlBh30'
genai.configure(api_key=GOOGLE_API_KEY)

# Create a blueprint for the API
team_api_bp = Blueprint('team_api', __name__)

@team_api_bp.route('/projects/<int:project_id>/teams', methods=['GET'])
def get_teams_with_milestones(project_id):
    # Query the project to ensure it exists
    project = Projects.query.get_or_404(project_id)
    
    # Query teams for the given project and load their related milestones and milestone trackers
    teams = Team.query.filter(Team.project_id == project.id).all()

    # Prepare the response data
    response_data = []

    for team in teams:
        # Prepare the milestones data for the team
        milestones_data = []
        for milestone in Milestones.query.filter(Milestones.project_id == project.id).all():
            # Get the milestone progress from MilestoneTracker
            milestone_tracker = MilestoneTracker.query.filter(
                MilestoneTracker.milestone_id == milestone.id,
                MilestoneTracker.team_id == team.id
            ).first()
            
            # Define the milestone status based on the tracker progress
            if milestone_tracker:
                if milestone_tracker.progress == 100:
                    status = 'Submitted'
                elif milestone_tracker.progress > 0:
                    status = 'In Progress'
                else:
                    status = 'Pending'
            else:
                status = 'Pending'
            
            # Add the milestone to the team milestones
            milestones_data.append({
                'id': milestone.id,
                'name': milestone.task,
                'status': status
            })
        
        # Add team data along with milestones to the response
        response_data.append({
            'id': team.id,
            'name': team.name,
            'milestones': milestones_data
        })

    # Return the final response as JSON
    return jsonify({'teams': response_data})


@team_api_bp.route('/projects/<int:project_id>/teams/<int:team_id>', methods=['GET'])
def get_team_with_commits(project_id, team_id):
    team = Team.query.options(joinedload(Team.members)).filter_by(id=team_id, project_id=project_id).first()
    
    if not team:
        return jsonify({"error": "Team not found"}), 404

    print(101, [i.id for i in team.members])
    response = {
        'team': {
            'id': team.id,
            'name': team.name,
            'members': [] #[i for i in team.members]
        }
    }

    # Initialize GitHubRepo class to fetch commits
    github_repo = GitHubRepo()

    for member in team.members:
        # Assuming you store the GitHub repo in the `repo_owner` field of Team
        git_user = GitUser.query.filter_by(userId=member.id).first()
        
        if git_user and team.repo_name:  # Access repo_name from Team
            # Fetch commits from the GitHub repository
            commit_response = github_repo.get(git_user.owner, team.repo_name)  # Now get the response
            commits = commit_response.get_json().get('commit_data', [])  # Extract the commit data from the response
        else:
            commits = []

        if commits:
            member_commits = commits[:5]  # Limit to 5 latest commits, modify as needed
            member_data = {
                'id': member.id,
                'name': member.username,
                'totalCommits': len(member_commits),
                'lastCommits': [{
                    'id': commit['sha'],
                    'date': commit['commit_date'],
                    'message': commit['message']
                } for commit in member_commits]
            }
        else:
            member_data = {
                'id': member.id,
                'name': member.username,
                'totalCommits': 0,
                'lastCommits': []
            }

        response['team']['members'].append(member_data)

    return jsonify(response)



@team_api_bp.route('/teams/<int:team_id>', methods=['GET'])
def get_team_info(team_id):
    # Retrieve the team by its ID, including related members and notifications
    team = Team.query.filter_by(id=team_id).first()  # .first() returns None if no team is found

    if not team:
        # If the team is not found, return a 404 error
        return jsonify({"error": "Team not found"}), 404

    # Prepare the response data for the team
    team_info = {
        'id': team.id,
        'name': team.name,
        'description': team.description,
        'project_id': team.project_id,
        'repo_owner': team.repo_owner,
        'repo_name': team.repo_name,
        'members': [{'id': member.id, 'username': member.username} for member in team.members],
        'notifications': [{'id': notification.id, 'title': notification.title, 'message': notification.message} for notification in team.notifications]
    }

    # Return the team information as a JSON response
    return jsonify(team_info)

# New Route for /teams/<int:team_id>/repo
@team_api_bp.route('/teams/<int:team_id>/repo', methods=['GET'])
def get_team_repo(team_id):
    # Retrieve the team by its ID from the Team model
    team = Team.query.filter_by(id=team_id).first()
    
    # If team is not found, return an error
    if not team:
        return jsonify({"message": f"Team with id {team_id} not found."}), 404
    
    # Extract repo_owner and repo_name from the team
    repo_owner = "githubtraining" #team.repo_owner
    repo_name = "github-slideshow-demo" #team.repo_name

    # Check if the GitHub owner exists using the check_owner_exists method
    github_repo = GitHubRepo()
    if not github_repo.check_owner_exists(repo_owner):
        return jsonify({"message": f"Owner '{repo_owner}' not found on GitHub."})

    commit_response = github_repo.get(repo_owner, repo_name)  # Now get the response
    commits = commit_response.get_json().get('commit_data', [])  # Extract the commit data from the response
        
    # Return the repo_owner and repo_name
    return commits

# Route to upload file
@team_api_bp.route('/upload/<int:team_id>/<int:user_id>/<int:milestone>', methods=['POST'])
def upload_file(team_id,user_id,milestone):
   if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"})

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"})

    # Secure the filename to prevent directory traversal
    filename = secure_filename(file.filename)

    # Read file data as binary
    file_data = file.read()
    print(f"Received file: {filename}, Size: {len(file_data)} bytes")

    # Placeholder for file_url (e.g., set a default or generate one)
    file_url = f"/uploaded_files/{filename}"

    # Save file data in database
    new_file = FileStorage(
        filename=filename,
        file_url=file_url,  # Use the placeholder or generate an actual URL
        file_data=file_data,
        uploaded_at=datetime.now(),
        uploaded_by=user_id,
        related_milestone=milestone,
        team_id=team_id
    )

    try:
        db.session.add(new_file)
        db.session.commit()
        return jsonify({"message": "File uploaded successfully", "file_id": new_file.id})
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        return jsonify({"error": str(e)})
        
@team_api_bp.route('/get_user_details/<int:user_id>', methods=['GET'])
def get_user_details(user_id):
    try:
        # Query all teams the user belongs to
        team_memberships = TeamMembers.query.filter_by(user_id=user_id).all()

        # If no teams found
        if not team_memberships:
            return jsonify({"error": "No teams found for the given user ID"}), 404

        # Retrieve team IDs and corresponding project IDs
        teams_and_projects = []
        for membership in team_memberships:
            team = Team.query.get(membership.team_id)
            if team:
                project = Projects.query.get(team.project_id)
                teams_and_projects.append({
                    "team_id": team.id,
                    "team_name": team.name,
                    "project_id": project.id if project else None,
                    "project_title": project.title if project else None
                })

        return jsonify({
            "user_id": user_id,
            "teams_and_projects": teams_and_projects,
            "team_id":team.id
        }), 200

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
