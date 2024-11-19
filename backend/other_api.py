# from celery import Celery
from backend.models import Notifications, db
from datetime import datetime, timedelta
from flask import current_app as app, jsonify, request, Blueprint
from flask_restful import Resource, Api, reqparse, marshal_with, fields
from .models import User, db, Projects, Milestones
import requests
from sqlalchemy import func,case

other_api_bp = Blueprint('other_api', __name__)

'''have to Replace https://genai-model.example.com/ with actual GenAI model URLs or APIs.
'''

api = Api()

# celery = Celery('tasks', broker='redis://localhost:6379/0')
# @celery.task
def send_reminder_notifications():
    # Find milestones due in 24 hours
    now = datetime.now()
    upcoming_milestones = Milestones.query.filter(
        Milestones.deadline.between(now, now + timedelta(hours=24))
    ).all()

    # Create notifications for each milestone
    for milestone in upcoming_milestones:
        notification = Notifications(
            title=f"Reminder: Upcoming Milestone",
            message=f"Milestone '{milestone.task}' is due on {milestone.deadline}.",
            created_for=milestone.project_id,
            created_by='System'
        )
        db.session.add(notification)

    db.session.commit()
    return "Reminders Sent"

class ReminderManager(Resource):
    def post(self):
        try:
            send_reminder_notifications.apply_async()
            return jsonify({'message': 'Reminder notifications sent successfully'}), 200
        except Exception as e:
            return jsonify({'ERROR': f'{e}'}), 400

api.add_resource(ReminderManager, '/reminders/send')

class SubmissionValidation(Resource):
    def post(self):
        data = request.get_json()
        required_fields = ['submission', 'project_id', 'milestone_id']
        if not all(field in data for field in required_fields):
            return jsonify({'message': 'Missing required fields'}), 400

        # Fetch milestone details
        milestone = Milestones.query.get(data['milestone_id'])
        if not milestone:
            return jsonify({'message': 'Milestone not found'}), 404

        # Call the GenAI model for validation
        genai_url = "https://genai-model.example.com/validate"
        payload = {
            "submission": data['submission'],
            "milestone_requirements": milestone.description
        }

        try:
            response = requests.post(genai_url, json=payload)
            if response.status_code == 200:
                validation_result = response.json()
                return jsonify({
                    'validation_result': validation_result,
                    'feedback': validation_result.get('feedback', 'No feedback provided')
                }), 200
            return jsonify({'message': 'Error from GenAI model'}), response.status_code
        except Exception as e:
            return jsonify({'ERROR': f'{e}'}), 500

api.add_resource(SubmissionValidation, '/submission/validate')

class PerformancePrediction(Resource):
    def post(self):
        data = request.get_json()
        if 'students_data' not in data:
            return jsonify({'message': 'Missing students data'}), 400

        # Call GenAI model to analyze performance
        genai_url = "https://genai-model.example.com/predict"
        try:
            response = requests.post(genai_url, json=data)
            if response.status_code == 200:
                prediction_results = response.json()
                return jsonify({'students_needing_support': prediction_results}), 200
            return jsonify({'message': 'Error from GenAI model'}), response.status_code
        except Exception as e:
            return jsonify({'ERROR': f'{e}'}), 500

api.add_resource(PerformancePrediction, '/students/performance-prediction')

class DocumentationChatbot(Resource):
    def post(self):
        data = request.get_json()
        if 'question' not in data:
            return jsonify({'message': 'Missing question field'}), 400

        # Call Chatbot API
        chatbot_url = "https://chatbot.example.com/answer"
        payload = {"question": data['question']}

        try:
            response = requests.post(chatbot_url, json=payload)
            if response.status_code == 200:
                chatbot_response = response.json()
                return jsonify({'response': chatbot_response['answer']}), 200
            return jsonify({'message': 'Error from chatbot API'}), response.status_code
        except Exception as e:
            return jsonify({'ERROR': f'{e}'}), 500

api.add_resource(DocumentationChatbot, '/chatbot/ask')

class TeamPerformance(Resource):
    def get(self):
        try:
            # Aggregate performance data
            teams = db.session.query(
                Projects.id,
                Projects.title,
                func.count(Milestones.id).label('total_milestones'),
                func.sum(
                    case([(Milestones.deadline < datetime.now(), 1)], else_=0)
                ).label('overdue_milestones')
            ).join(Milestones).group_by(Projects.id).all()

            team_data = [{
                'team_id': team[0],
                'team_name': team[1],
                'total_milestones': team[2],
                'overdue_milestones': team[3]
            } for team in teams]

            return jsonify({'teams': team_data}), 200
        except Exception as e:
            return jsonify({'ERROR': f'{e}'}), 500

api.add_resource(TeamPerformance, '/teams/performance')

class InstructorFeedbackNotifications(Resource):
    def get(self, project_id):
        try:
            notifications = Notifications.query.filter_by(created_for=project_id).all()
            feedback = [{
                'id': notif.id,
                'title': notif.title,
                'message': notif.message,
                'created_at': notif.created_at
            } for notif in notifications]

            return jsonify({'feedback_notifications': feedback}), 200
        except Exception as e:
            return jsonify({'ERROR': f'{e}'}), 500

api.add_resource(InstructorFeedbackNotifications, '/feedback/<int:project_id>')
