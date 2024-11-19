from flask import current_app as app, jsonify, request, Blueprint
from .models import User, db, Projects, Milestones
import spacy

chatbot_bp = Blueprint('chatbot', __name__)

# Load spaCy model
nlp = spacy.load('en_core_web_sm')

def project_not_found():
    return jsonify({"message": "Project not found."}), 404

def milestone_not_found():
    return jsonify({"message": "Milestone not found."}), 404

def get_project_by_title(title):
    return Projects.query.filter(Projects.title.ilike(title)).first()

def get_milestone_by_project_and_task(project_id, task_name):
    return Milestones.query.filter_by(project_id=project_id, task=task_name).first()

@app.route('/chatbot', methods=['POST'])
def chatbot():
    user_input = request.json.get('message', '')

    # Use spaCy to process the input
    doc = nlp(user_input)

    # Extract entities using spaCy (assuming project and milestone are proper nouns or named entities)
    project_title = None
    milestone_name = None

    for ent in doc.ents:
        if ent.label_ == "ORG":  # assuming the project title is an organization or named entity
            project_title = ent.text
        elif ent.label_ == "PRODUCT":  # assuming milestone names are recognized as products
            milestone_name = ent.text
    
    if project_title and milestone_name:
        # Fetch the project from the database
        project = get_project_by_title(project_title)
        if project:
            # Fetch the milestone by project ID and task name
            milestone = get_milestone_by_project_and_task(project.id, milestone_name)
            if milestone:
                # Return the deadline of the milestone
                return jsonify({"deadline": milestone.deadline.isoformat()})
            else:
                return milestone_not_found()
        else:
            return project_not_found()

    return jsonify({"message": "I didn't understand your question."}), 400
