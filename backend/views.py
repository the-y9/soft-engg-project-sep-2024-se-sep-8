from flask import current_app as app, jsonify,request, render_template, send_file
from flask_security import auth_required, roles_required
from werkzeug.security import check_password_hash,generate_password_hash
from backend.security import datastore 
from flask_restful import marshal, fields
import flask_excel as excel
from .models import User, db
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
    if datastore.find_user(email=data.get('email')):
        return jsonify({'message': 'Email already registered'}), 400 
    if not data.get("password"):
        return jsonify({"message":"Password not provided"}),400
       
    try:
        datastore.create_user(
            email=data['email'],
            password=generate_password_hash(data['password']),
            roles=['student'],  
            active=False
        )
        db.session.commit()
        return jsonify({'message': 'Successfully registered as student.'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500
    


@app.post('/user-login')
def user_login():
    data = request.get_json()
    email = data.get('email')
    if not email:
        return jsonify({"message":"Email not provided"}),400
    if not data.get("password"):
        return jsonify({"message":"Password not provided"}),400
    
    user = datastore.find_user(email=email)
    
    if not user:
        return jsonify({"message":"Email not found."}),404
    
    if check_password_hash(user.password, data.get("password")):
        if user.active:
            return jsonify({"token":user.get_auth_token(),"email":user.email,"role":user.roles[0].name}),200
        else:
            return jsonify({"message":"User not activated"}),403
    
    else: 
        return jsonify({"message":"Wrong password"}),400
    
