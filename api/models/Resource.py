from app import db
from .User import User
from .Department import Department
from datetime import datetime
from .Base import Base


class Resource(db.Model, Base):
    __tablename__ = 'resources'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(125), nullable=False)
    description = db.Column(db.String(255))
    data = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    dept_id = db.Column(db.ForeignKey(Department.id))
    department = db.relationship(Department, back_populates='resources')
    user_id = db.Column(db.ForeignKey(User.id))
    user = db.relationship(User, back_populates='resources')
