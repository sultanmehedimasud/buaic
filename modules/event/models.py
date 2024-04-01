from flask_bcrypt import Bcrypt
from datetime import datetime
from extensions import db, login_manager, migrate 

bcrypt = Bcrypt()

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    venue = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    def get_event(self):
        return str(self.id, self.title, self.description, self.date, self.venue, self.created_at)

