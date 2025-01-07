from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initialize the Flask application
app = Flask(__name__)

# Application configurations
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'outputs'
app.config['SECRET_KEY'] = 'test hard secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/malcolmorian/Documents/Bioinformatics/Projects2024/Seqsure/seqsure/seqsure.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Add application context for database initialization or other tasks
with app.app_context():
    # Import models and routes after initializing `db` and `app`
    from .models import User  # Ensure this is correctly defined in your models.py
    import app.routes as routes  # Ensure this is correctly defined in your routes.py
    db.create_all()  # Create all database tables
        
# Run the application
if __name__ == "__main__":
    # Start the Flask application
    app.run(debug=True, host="0.0.0.0", port=5000)

