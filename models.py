from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Recipe(db.Model):
    __tablename__ = "recipes"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String,  nullable=False)
    making_time = db.Column(db.String,  nullable=False)
    serves = db.Column(db.String,  nullable=False)
    ingredients = db.Column(db.String,  nullable=False)
    cost = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.String,  nullable=False)
    updated_at = db.Column(db.String,  nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "making_time": self.making_time,
            "serves": self.serves,
            "ingredients": self.ingredients,
            "cost": str(self.cost),
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @staticmethod
    def now():
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
