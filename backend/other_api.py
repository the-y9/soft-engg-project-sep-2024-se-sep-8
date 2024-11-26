# from celery import Celery
from backend.models import Notifications, db
from datetime import datetime, timedelta
from flask import current_app as app, jsonify, request, Blueprint
from flask_restful import Resource, Api, reqparse, marshal_with, fields
from .models import User, db, Projects, Milestones,Team, TeamMembers, EvaluationCriteria, PeerReview, SystemLog
import requests
from sqlalchemy import func,case
import google.generativeai as genai

other_api_bp = Blueprint('other_api', __name__)

'''have to Replace https://genai-model.example.com/ with actual GenAI model URLs or APIs.
'''

api = Api(other_api_bp)

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
            return jsonify({'message': 'Error from GenAI model'}), response.status_code, 500
        except Exception as e:
            return jsonify({'ERROR': f'{e}'}), 500

api.add_resource(PerformancePrediction, '/students/performance-prediction')

class DocumentationChatbot(Resource):
    def post(self):
        data = request.get_json()

        # Check if 'question' and 'api_key' fields are present
        if 'question' not in data or 'api_key' not in data:
            return jsonify({'message': 'Missing question or api_key field'}), 400

        question = data['question']
        api_key = data['api_key']

        try:
            # Configure Gemini API dynamically with the provided API key
            genai.configure(api_key=api_key)

            # Generate a response using the Gemini API
            model = genai.GenerativeModel(model_name="gemini-1.5-flash")
            response = model.generate_content(question)
            answer = response.text

            return jsonify({'response': answer}), 200
        
        except genai.exceptions.InvalidApiKeyError:
            return jsonify({'error': 'Invalid API Key'}), 401
        except Exception as e:
            return jsonify({'ERROR': str(e)}), 500
        
api.add_resource(DocumentationChatbot, '/chatbot/ask')

# will be dited
class TeamPerformance(Resource):
    def get(self):
        try:
            # Aggregate performance data
            teams = db.session.query(
                Team.id.label('team_id'),
                Team.name.label('team_name'),
                func.count(Milestones.id).label('total_milestones'),
                func.sum(
                    case(
                        [
                            (Milestones.deadline < datetime.now(), 1)
                        ], 
                        else_=0
                    )
                ).label('overdue_milestones')
            ).join(TeamMembers, TeamMembers.team_id == Team.id) \
             .join(User, TeamMembers.user_id == User.id) \
             .join(Projects, Projects.id == Team.project_id) \
             .join(Milestones, Milestones.project_id == Projects.id) \
             .group_by(Team.id).all()

            # Prepare response data
            team_data = [{
                'team_id': team[0],
                'team_name': team[1],
                'total_milestones': team[2],
                'overdue_milestones': team[3]
            } for team in teams]

            return jsonify({'teams': team_data})

        except Exception as e:
            return jsonify({'ERROR': f'{e}'})


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

            return jsonify({'feedback_notifications': feedback})
        except Exception as e:
            return jsonify({'ERROR': f'{e}'})

api.add_resource(InstructorFeedbackNotifications, '/feedback/<int:project_id>')

# Peer Review: Add Evaluation Criteria
class AddEvaluationCriteria(Resource):
    def post(self, projectId):
        data = request.get_json()
        if 'criteriaList' not in data:
            return jsonify({'message': 'Invalid data format. Please provide a valid criteria list.'}), 400

        try:
            project = Projects.query.get(projectId)
            if not project:
                return jsonify({'message': f'Project with ID {projectId} not found.'}), 404

            criteria_objects = []
            for item in data['criteriaList']:
                criterion = item.get('criterion')
                description = item.get('description', '')
                if not criterion:
                    return jsonify({'message': 'Each criterion must have a name.'}), 400
                criteria_objects.append(EvaluationCriteria(project_id=projectId, criterion=criterion, description=description))

            db.session.add_all(criteria_objects)
            db.session.commit()

            return jsonify({
                'message': 'Evaluation criteria added successfully',
                'projectId': projectId,
                'criteria': [{'id': c.id, 'criterion': c.criterion, 'description': c.description} for c in criteria_objects]
            }), 201

        except Exception as e:
            db.session.rollback()
            return jsonify({'message': f'An error occurred: {str(e)}'}), 500

api.add_resource(AddEvaluationCriteria, '/project/<int:projectId>/evaluation-criteria')

# Peer Review: Submit Peer Review
class SubmitPeerReview(Resource):
    def post(self):
        data = request.get_json()
        required_fields = ['reviewerId', 'projectId', 'criteria']

        if not all(field in data for field in required_fields):
            return jsonify({'message': 'Invalid request data.'}), 400

        try:
            peer_review = PeerReview(
                reviewer_id=data['reviewerId'],
                project_id=data['projectId'],
                criteria=data['criteria']
            )
            db.session.add(peer_review)
            db.session.commit()

            return jsonify({'message': 'Peer review submitted successfully.', 'reviewId': peer_review.id}), 201

        except Exception as e:
            db.session.rollback()
            return jsonify({'message': f'An error occurred: {str(e)}'}), 500

api.add_resource(SubmitPeerReview, '/peer-review')

# Peer Review: Retrieve Peer Reviews
class RetrievePeerReviews(Resource):
    def get(self, projectId):
        try:
            reviews = PeerReview.query.filter_by(project_id=projectId).all()
            if not reviews:
                return jsonify({'message': f'No peer reviews found for project ID {projectId}.'}), 404

            return jsonify({
                'projectId': projectId,
                'reviews': [
                    {
                        'reviewerId': review.reviewer_id,
                        'criteria': review.criteria,
                        'created_at': review.created_at
                    } for review in reviews
                ]
            }), 200

        except Exception as e:
            return jsonify({'message': f'An error occurred: {str(e)}'}), 500

api.add_resource(RetrievePeerReviews, '/peer-review/project/<int:projectId>')

# Peer Review: Edit Peer Review
class EditPeerReview(Resource):
    def put(self, reviewId):
        data = request.get_json()
        if 'criteria' not in data:
            return jsonify({'message': 'Invalid request data.'}), 400

        try:
            review = PeerReview.query.get(reviewId)
            if not review:
                return jsonify({'message': 'Peer review not found.'}), 404

            review.criteria = data['criteria']
            db.session.commit()

            return jsonify({'message': 'Peer review updated successfully.'}), 200

        except Exception as e:
            db.session.rollback()
            return jsonify({'message': f'An error occurred: {str(e)}'}), 500

api.add_resource(EditPeerReview, '/peer-review/<int:reviewId>')

# Peer Review: Delete Peer Review
class DeletePeerReview(Resource):
    def delete(self, reviewId):
        try:
            review = PeerReview.query.get(reviewId)
            if not review:
                return jsonify({'message': 'Peer review not found.'}), 404

            db.session.delete(review)
            db.session.commit()

            return jsonify({'message': 'Peer review deleted successfully.'}), 200

        except Exception as e:
            db.session.rollback()
            return jsonify({'message': f'An error occurred: {str(e)}'}), 500

api.add_resource(DeletePeerReview, '/peer-review/<int:reviewId>')

class RetrieveLogs(Resource):
    def get(self):
        try:
            # Retrieve query parameters
            start_date = request.args.get('start_date')
            end_date = request.args.get('end_date')
            severity = request.args.get('severity')

            # Base query
            query = SystemLog.query

            # Add filters if provided
            if start_date:
                query = query.filter(SystemLog.timestamp >= start_date)
            if end_date:
                query = query.filter(SystemLog.timestamp <= end_date)
            if severity:
                query = query.filter(SystemLog.severity.ilike(severity))

            # Execute query
            logs = query.order_by(SystemLog.timestamp.asc()).all()

            # Prepare response
            log_data = [
                {
                    'timestamp': log.timestamp.isoformat(),
                    'severity': log.severity,
                    'message': log.message
                }
                for log in logs
            ]

            return jsonify(log_data), 200

        except Exception as e:
            return jsonify({'ERROR': str(e)}), 500

api.add_resource(RetrieveLogs, '/logs')
class SearchLogs(Resource):
    def post(self):
        try:
            # Parse request body
            data = request.get_json()

            if not data or 'keyword' not in data:
                return jsonify({'message': 'Keyword is required for searching logs.'}), 400

            keyword = data['keyword']

            # Perform case-insensitive search
            logs = SystemLog.query.filter(SystemLog.message.ilike(f"%{keyword}%")).all()

            # Prepare response
            search_results = [
                {
                    'timestamp': log.timestamp.isoformat(),
                    'severity': log.severity,
                    'message': log.message
                }
                for log in logs
            ]

            return jsonify(search_results), 200

        except Exception as e:
            return jsonify({'ERROR': str(e)}), 500


api.add_resource(SearchLogs, '/logs/search')