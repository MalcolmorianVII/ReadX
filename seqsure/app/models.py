from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime
from app import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False, index=True)
    job_title = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    sequencing_runs = db.relationship('SequencingRun', backref='user', lazy=True)


class SequencingRun(db.Model):
    __tablename__ = 'sequencing_runs'
    id = db.Column(db.Integer, primary_key=True)
    run_name = db.Column(db.String(255), nullable=False, unique=True, index=True)
    run_date = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(50), nullable=False, default='Pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    samples = db.relationship('Sample', backref='sequencing_run', lazy=True)
    qc_metrics = db.relationship('QCMetrics', backref='sequencing_run', lazy=True)


class Sample(db.Model):
    __tablename__ = 'samples'
    id = db.Column(db.Integer, primary_key=True)
    sequencing_run_id = db.Column(db.Integer, db.ForeignKey('sequencing_runs.id'), nullable=False)
    sample_name = db.Column(db.String(255), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True, default="")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    pipeline_results = db.relationship('PipelineResult', backref='sample', lazy=True)
    qc_metrics = db.relationship('QCMetrics', backref='sample', lazy=True)


class PipelineResult(db.Model):
    __tablename__ = 'pipeline_results'
    id = db.Column(db.Integer, primary_key=True)
    sample_id = db.Column(db.Integer, db.ForeignKey('samples.id'), nullable=False)
    metric_value = db.Column(db.Text, nullable=True)  # Expanded to allow larger results
    generated_at = db.Column(db.DateTime, default=datetime.utcnow)


class QCMetrics(db.Model):
    __tablename__ = 'qc_metrics'
    id = db.Column(db.Integer, primary_key=True)
    sequencing_run_id = db.Column(db.Integer, db.ForeignKey('sequencing_runs.id'), nullable=False)
    sample_id = db.Column(db.Integer, db.ForeignKey('samples.id'), nullable=False)
    avg_q_score = db.Column(db.Float, db.CheckConstraint('avg_q_score >= 0'), nullable=True)  # Must be non-negative
    avg_depth = db.Column(db.Float, db.CheckConstraint('avg_depth >= 0'), nullable=True)
    percentage_10X = db.Column(
        db.Float, 
        db.CheckConstraint('percentage_10X >= 0 AND percentage_10X <= 100'),
        nullable=True
    )
    percentage_30X = db.Column(
        db.Float, 
        db.CheckConstraint('percentage_30X >= 0 AND percentage_30X <= 100'),
        nullable=True
    )
    total_reads = db.Column(db.Integer, db.CheckConstraint('total_reads >= 0'), nullable=True)
    reads_mapped = db.Column(db.Integer, db.CheckConstraint('reads_mapped >= 0'), nullable=True)
    percentage_reads_mapped = db.Column(
        db.Float, 
        db.CheckConstraint('percentage_reads_mapped >= 0 AND percentage_reads_mapped <= 100'),
        nullable=True
    )
    total_assembly_length = db.Column(db.Integer, db.CheckConstraint('total_assembly_length >= 0'), nullable=True)
    total_contigs = db.Column(db.Integer, db.CheckConstraint('total_contigs >= 0'), nullable=True)
    n50 = db.Column(db.Integer, db.CheckConstraint('n50 >= 0'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
