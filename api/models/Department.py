from app import db
from .Base import Base


class Department(db.Model, Base):
    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    cover_pic = db.Column(db.String(255))

    resources = db.relationship('Resource', order_by='Resource.title',
                                back_populates="department",
                                cascade="all, delete, delete-orphan")
