from app import db
from .Role import Role
from .Base import Base


class User(db.Model, Base):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    profile_pic = db.Column(db.String(255))

    role_id = db.Column(db.ForeignKey(Role.id))
    role = db.relationship(Role, back_populates='users')

    resources = db.relationship('Resource', order_by='Resource.title',
                                back_populates="user",
                                cascade="all, delete, delete-orphan")

    def __repr__(self):
        return f'<User "{self.username}"-{self.email}>'
