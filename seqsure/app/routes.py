import os
from flask import (
    render_template, redirect, url_for, flash, request, 
    jsonify, current_app, Blueprint, send_from_directory,flash
)
from werkzeug.utils import secure_filename
from .pipeline_handler import run_nextflow_pipeline
from .forms import LoginForm, RegisterForm

# Create a Blueprint for routing
routes = Blueprint('routes', __name__)

# Routes
@current_app.route('/', methods=['GET'])
def home():
    """Serve the home page."""
    return render_template('home.html')

@current_app.route('/index', methods=['GET', 'POST'])
def index():
    """Serve the index page."""
    return render_template('index.html')

@current_app.route('/register', methods=['GET', 'POST'])
def register():
    """Serve the registration page."""
    form = RegisterForm()
    user = None  # Placeholder for user data
    if form.validate_on_submit():
        # Register user in the database
        form_data = {
            "title": form.title.data,
            "email": form.email.data,
            "password": form.password.data
        }
        # Reset form fields for demonstration purposes
        form_data = {key: '' for key in form_data}
        flash('Registration successful!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', form=form, user=user)

@current_app.route('/login', methods=['GET', 'POST'])
def login():
    """Serve the login page."""
    form = LoginForm()
    if form.validate_on_submit():
        # Example logic for handling login
        login_data = {
            "email": form.email.data,
            "password": form.password.data
        }
        # Reset login fields for demonstration purposes
        login_data = {key: '' for key in login_data}
        return redirect(url_for('home'))
    return render_template('login.html', form=form)

@current_app.route('/seqsure', methods=['GET', 'POST'])
def seqsure():
    """Serve the Seqsure page."""
    return render_template('seqsure.html', title="Run Seqsure")

@current_app.route('/data', methods=['GET', 'POST'])
def data():
    """Serve the Data page."""
    return render_template('data.html', title="Data")

@current_app.route('/results', methods=['GET', 'POST'])
def results():
    """Serve the Results page."""
    return render_template('results.html', title="Results")

@current_app.route('/uploads', methods=['POST'])
def upload_file():
    """Handle file uploads."""
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    filename = secure_filename(file.filename)
    upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    file.save(upload_path)
    return jsonify({'message': 'File uploaded successfully', 'filename': filename}), 200

@current_app.route('/run_pipeline', methods=['POST'])
def run_pipeline():
    """Run the Nextflow pipeline."""
    data = request.json
    input_file = os.path.join(current_app.config['UPLOAD_FOLDER'], data.get('filename'))
    output_dir = current_app.config['OUTPUT_FOLDER']
    
    if not os.path.exists(input_file):
        return jsonify({'error': 'Input file not found'}), 400
    
    result = run_nextflow_pipeline(input_file, output_dir)
    if result['success']:
        return jsonify({'message': 'Pipeline executed successfully', 'output': result['stdout']}), 200
    return jsonify({'error': 'Pipeline execution failed', 'stderr': result['stderr']}), 500
