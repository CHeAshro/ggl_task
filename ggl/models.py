
from app import db


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    status = db.Column(db.Boolean, nullable=False, default=False)

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'status': int(self.status),
        }
