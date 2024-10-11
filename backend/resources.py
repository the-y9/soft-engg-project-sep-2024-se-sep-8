from flask_restful import Resource, Api, reqparse, marshal_with, fields
from flask_security import auth_required, roles_required, current_user
from backend.models import db
from sqlalchemy import func
from flask import jsonify
from .instance import cache
from .models import User, GitUser
import requests



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
        token=key("rough@g.com")
        """Handles both checking if the owner exists and getting repository commits."""
        
        if not self.check_owner_exists(owner):
            return jsonify({"message": f"Owner '{owner}' not found on GitHub."})

        if not repo:
            return jsonify({"message": f"'{owner}' is a valid owner name."})

        try:
            token
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
