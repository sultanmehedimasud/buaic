from app import db


class Semester(db.Model):
    semester_name = db.Column(db.String(100), primary_key=True)
    recruitment_started = db.Column(db.DateTime)
    recruitment_end = db.Column(db.DateTime)
    recruitment_status = db.Column(db.Boolean, default=False)

def create_semester(semester_name, recruitment_started, recruitment_end, recruitment_status=False):
    semester = Semester(
        semester_name=semester_name,
        recruitment_started=recruitment_started,
        recruitment_end=recruitment_end,
        recruitment_status=recruitment_status
    )
    db.session.add(semester)
    db.session.commit()