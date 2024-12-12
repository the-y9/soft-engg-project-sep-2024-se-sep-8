from flask import current_app as app, jsonify,request, render_template, send_file
from flask_security import auth_required, roles_required
from werkzeug.security import check_password_hash,generate_password_hash
from backend.security import datastore 
from flask_restful import marshal, fields
import flask_excel as excel
from .models import User, db , TeamMembers
# from .chatbot import chatbot_bp
from sqlalchemy import or_ 
import smtplib

@app.get('/')
def home():
    return render_template('index.html')

@app.get('/admin')
@auth_required("token")
@roles_required("admin")
def admin():
    return "Welcome admin"

@app.post('/user-signup')
def signup():
    data = request.get_json()
    if datastore.find_user(email=data.get('email')): # or datastore.find_user(username=data.get('email')):
        return jsonify({'message': 'Email already registered'})
    if not data.get("password"):
        return jsonify({"message":"Password not provided"})
       
    try:
        datastore.create_user(
            email=data['email'],
            username=data['username'],
            password=generate_password_hash(data['password']),
            roles=['student'],  
            active=True
        )
        db.session.commit()
        return jsonify({'message': 'Successfully registered as student.'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error occurred while creating the user account - ' + str(e)})
    


@app.post('/user-login')
def user_login():
    data = request.get_json()
    email = data.get('email')
    print(email)
    if not email:
        return jsonify({"message":"Email or Username not provided"})
    if not data.get("password"):
        return jsonify({"message":"Password not provided"})
    
    if '@' in email:
        user = datastore.find_user(email=email)
        print(1)
    else:
        print(2)
        user = datastore.find_user(username=email)
    
    if not user:
        return jsonify({"message":"Email or Username not found."})
    
    if check_password_hash(user.password, data.get("password")):
        if user.active:
            # return jsonify({"token":user.get_auth_token(),"id":user.id,"email":user.email,"role":user.roles[0].name}),200
            team_member = TeamMembers.query.filter_by(user_id=user.id).first()
            team_id = team_member.team_id if team_member else None
            
            return jsonify({"token":user.get_auth_token(),"id":user.id,"email":user.email,"role":user.roles[0].name,  "team_id": team_id})
        else:
            return jsonify({"message":"User not activated"})
    
    else: 
        return jsonify({"message":"Wrong password"})


@app.post('/upload')
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'})

    file = request.files['file']
    milestone_id = request.form.get('milestoneId')

    if not file:
        return jsonify({'error': 'File is required'})
    try:
        file.save(f'uploads/{milestone_id}_{file.filename}')
        return jsonify({'message': 'File uploaded successfully'})
    except Exception as e:
        return jsonify({'error': str(e)})

    
