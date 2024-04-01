from flask_bcrypt import Bcrypt
from datetime import datetime
from extensions import db, login_manager, migrate 

bcrypt = Bcrypt()

class Polls(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(100), nullable=False)
    option1 = db.Column(db.String(100), nullable=False)
    option2 = db.Column(db.String(100), nullable=False)
    option3 = db.Column(db.String(100), nullable=True)
    option4 = db.Column(db.String(100), nullable=True)
    count_option1 = db.Column(db.Integer, nullable=False, default=0)
    count_option2 = db.Column(db.Integer, nullable=False, default=0)
    count_option3 = db.Column(db.Integer, nullable=True, default=0)
    count_option4 = db.Column(db.Integer, nullable=True, default=0)
    # correct_option = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    def get_poll(self):
        return str(self.id, self.question, self.option1, self.option2, self.option3, self.option4, self.count_option1, self.count_option2, self.count_option3, self.count_option4, self.created_at)
