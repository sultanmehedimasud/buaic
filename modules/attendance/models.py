from datetime import datetime

from app import db


class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.now)

    student_id = db.Column(db.Integer, db.ForeignKey('user.student_id'), nullable=False)
    user = db.relationship('User', backref=db.backref('attendance', lazy=True))
    
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    event = db.relationship('Event', backref=db.backref('attendance', lazy=True))
