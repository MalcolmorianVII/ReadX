from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime
from app import db

# db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    job_title = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    # created_at = db.Column(db.DateTime, default=datetime.utcnow)
    #sequencing_runs = db.relationship('SequencingRun', backref='user', lazy=True)

class SequencingRun(db.Model):
    __tablename__ = 'sequencing_runs'
    id = db.Column(db.Integer, primary_key=True)
    run_name = db.Column(db.String(255), nullable=False)
    run_date = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    status = db.Column(db.String(50), nullable=False, default='Pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    samples = db.relationship('Sample', backref='sequencing_run', lazy=True)
    logs = db.relationship('Log', backref='sequencing_run', lazy=True)

class Sample(db.Model):
    __tablename__ = 'samples'
    id = db.Column(db.Integer, primary_key=True)
    sequencing_run_id = db.Column(db.Integer, db.ForeignKey('sequencing_runs.id'), nullable=False)
    sample_name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    pipeline_results = db.relationship('PipelineResult', backref='sample', lazy=True)

class PipelineResult(db.Model):
    __tablename__ = 'pipeline_results'
    id = db.Column(db.Integer, primary_key=True)
    sample_id = db.Column(db.Integer, db.ForeignKey('samples.id'), nullable=False)
    metric_id = db.Column(db.Integer, db.ForeignKey('qc_metrics.id'), nullable=False)
    metric_value = db.Column(db.String(255), nullable=True)
    generated_at = db.Column(db.DateTime, default=datetime.utcnow)

class QCMetrics(db.Model):
    __tablename__ = 'qc_metrics'
    id = db.Column(db.Integer, primary_key=True)
    sample_id = db.Column(db.Integer, db.ForeignKey('samples.id'), nullable=False)
    avg_q_score = db.Column(db.Float, nullable=True)  # Phred Quality Score
    avg_depth = db.Column(db.Float, nullable=True)  # Average sequencing depth
    percentage_10X = db.Column(db.Float, nullable=True)  # Percentage of regions covered at 10X
    percentage_30X = db.Column(db.Float, nullable=True)  # Percentage of regions covered at 30X
    total_reads = db.Column(db.Integer, nullable=True)  # Total number of reads
    reads_mapped = db.Column(db.Integer, nullable=True)  # Total number of mapped reads
    percentage_reads_mapped = db.Column(db.Float, nullable=True)  # Percentage of reads mapped
    total_assembly_length = db.Column(db.Integer, nullable=True)  # Total length of the assembly
    total_contigs = db.Column(db.Integer, nullable=True)  # Number of contigs
    n50 = db.Column(db.Integer, nullable=True)  # N50 of the assembly
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship
    sample = db.relationship('Sample', backref=db.backref('qc_metrics', lazy=True))


class Log(db.Model):
    __tablename__ = 'logs'
    id = db.Column(db.Integer, primary_key=True)
    sequencing_run_id = db.Column(db.Integer, db.ForeignKey('sequencing_runs.id'), nullable=False)
    log_message = db.Column(db.Text, nullable=False)
    log_level = db.Column(db.String(50), nullable=False, default='INFO')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
