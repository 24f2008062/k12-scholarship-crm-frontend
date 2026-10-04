"""
Database models for K12 Hunar Scholarship Management CRM.
"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Allowed constants for validation and filtering
ALLOWED_STATES = ["Bihar", "Haryana", "Jharkhand"]
ALLOWED_STATUSES = ["Published", "Draft", "Expired"]


class Scholarship(db.Model):
    """
    Represents a scholarship record managed in the CRM.
    """
    __tablename__ = "scholarships"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    provider_name = db.Column(db.String(200), nullable=False)
    applicable_class = db.Column(db.String(100), nullable=False)
    eligibility_criteria = db.Column(db.Text, nullable=True)
    benefit = db.Column(db.Text, nullable=True)
    deadline = db.Column(db.String(100), nullable=True)  # Stores formatted date or 'Not stated'
    application_link = db.Column(db.String(500), nullable=True)
    status = db.Column(db.String(20), nullable=False, default="Draft")

    def __repr__(self):
        return f"<Scholarship id={self.id} name='{self.name}' state='{self.state}' status='{self.status}'>"
