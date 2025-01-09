import os
from app import app,db
from app.models import User

from flask import (
    render_template, redirect, url_for, flash, request, 
    jsonify, current_app, Blueprint, send_from_directory,flash
)
from werkzeug.utils import secure_filename
from .pipeline_handler import run_nextflow_pipeline
from .forms import LoginForm, RegisterForm
import bcrypt

# Hash a password
def hash_password(plain_password: str) -> str:
    # Generate a salt and hash the password
    hashed_password = bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password.decode('utf-8')

# Verify a password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

# Create a Blueprint for routing
#routes = Blueprint('routes', __name__)

# Routes
@app.route('/')
def home():
    """Serve the home page."""
    # Test querying the db & rendering info
    users = User.query.first()
    password = 'XXX123'
    user = 'yoak'
    return render_template('home.html',user=user,password=password)

@app.route('/index', methods=['GET', 'POST'])
def index():
    """Serve the index page."""
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Serve the registration page."""
    form = RegisterForm()
    #user = None  # Placeholder for user data
    if form.validate_on_submit():
        # Register user in the database
        form_data = {
            #"username": form.username.data, add this in RegisterForm
            "job_title": form.job_title.data,
            "email": form.email.data
        }
        form_data["username"] = form_data["email"].split('@')[0]
        # Check if user already exists in the database
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('User with email already exists', 'error')
            return redirect(url_for('register'))
        # Hash the password
        form_data["password_hash"] = hash_password(form.password.data)
        # Commit changes to the database
        user = User(**form_data)
        db.session.add(user)
        db.session.commit()
        
        form_data = {key: '' for key in form_data} # Reset form fields for demonstration purposes
        flash(f'You have registered successfully on ReadX,{user.username}!', 'success') 
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Serve the login page."""
    form = LoginForm()
    if form.validate_on_submit():
        # Example logic for handling login
        login_data = {
            "email": form.email.data,
            "password": form.password.data
        }
        # validate the login credentials
        user = User.query.filter_by(email=login_data["email"]).first()
        if not user or not verify_password(login_data["password"], user.password_hash):
            flash('Invalid login credentials', 'error')
            return redirect(url_for('login'))
        # Reset login fields for demonstration purposes
        login_data = {key: '' for key in login_data}
        return redirect(url_for('home'))
    return render_template('login.html', form=form)

@app.route('/seqsure', methods=['GET', 'POST'])
def seqsure():
    """Serve the Seqsure page."""
    return render_template('seqsure.html', title="Run Seqsure")

@app.route('/data', methods=['GET', 'POST'])
def data():
    """Serve the Data page."""
    return render_template('data.html', title="Data")

@app.route('/results', methods=['GET', 'POST'])
def results():
    """Serve the Results page."""
    return render_template('results.html', title="Results")

@app.route('/uploads', methods=['POST'])
def upload_file():
    """Handle file uploads."""
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    filename = secure_filename(file.filename)
    upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(upload_path)
    return jsonify({'message': 'File uploaded successfully', 'filename': filename}), 200

@app.route('/run_pipeline', methods=['POST'])
def run_pipeline():
    """Run the Nextflow pipeline."""
    data = request.json
    input_file = os.path.join(app.config['UPLOAD_FOLDER'], data.get('filename'))
    output_dir = app.config['OUTPUT_FOLDER']
    
    if not os.path.exists(input_file):
        return jsonify({'error': 'Input file not found'}), 400
    
    result = run_nextflow_pipeline(input_file, output_dir)
    if result['success']:
        return jsonify({'message': 'Pipeline executed successfully', 'output': result['stdout']}), 200
    return jsonify({'error': 'Pipeline execution failed', 'stderr': result['stderr']}), 500
