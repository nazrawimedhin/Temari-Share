from app import db
from .Base import Base


class Role(db.Model, Base):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    users = db.relationship('User', order_by='User.username')
