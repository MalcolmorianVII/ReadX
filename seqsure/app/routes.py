import os
from flask import render_template,redirect,url_for,flash,request, jsonify, current_app,Blueprint, send_from_directory
from werkzeug.utils import secure_filename
from .pipeline_handler import run_nextflow_pipeline
from .forms import LoginForm,RegisterForm

routes = Blueprint('routes', __name__)

# Serve the home page
@current_app.route('/', methods=['GET','POST'])
def home():
    # Serve the index.html file
    user=None
    form = RegisterForm()
    if form.validate_on_submit():
        title = form.title.data
        email = form.email.data
        password = form.password.data
        title = email = password = ''
        return redirect(url_for('home'))
    return render_template('forms.html',form=form,user=user)

# Serve the login page
@current_app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        email = password = ''
        return redirect(url_for('home'))
    return render_template('login.html',form=form)
# Serve the seqsure page
@current_app.route('/seqsure', methods=['GET','POST'])
def seqsure():
    title="Run seqsure"
    return render_template('seqsure.html',title=title)

# Serve the Data page
@current_app.route('/data', methods=['GET','POST'])
def data():
    title="Data"
    return render_template('data.html',title=title)

# Serve the Results page
@current_app.route('/results', methods=['GET','POST'])
def results():
    title="Results"
    return render_template('results.html',title=title)

# Serve the Results page
@current_app.route('/registration', methods=['GET','POST'])
def register():
    title="Register"
    # Get user credentials i.e username & pwd & store the user in the db
    # Give status i.e fail or success but either way redirect to login page 
    return render_template('register.html',title=title)

@current_app.route('/uploads', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file:
        filename = secure_filename(file.filename)
        upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(upload_path)
        return jsonify({'message': 'File uploaded successfully', 'filename': filename}), 200


@current_app.route('/run_pipeline', methods=['POST'])
def run_pipeline():
    data = request.json
    input_file = os.path.join(current_app.config['UPLOAD_FOLDER'], data.get('filename'))
    output_dir = current_app.config['OUTPUT_FOLDER']
    
    if not os.path.exists(input_file):
        return jsonify({'error': 'Input file not found'}), 400
    
    result = run_nextflow_pipeline(input_file, output_dir)
    
    if result['success']:
        return jsonify({'message': 'Pipeline executed successfully', 'output': result['stdout']}), 200
    else:
        return jsonify({'error': 'Pipeline execution failed', 'stderr': result['stderr']}), 500
