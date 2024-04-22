from datetime import datetime

from flask import Blueprint, flash, redirect, render_template, request, url_for

from . import intake_bp
from .models import Semester, create_semester

intake_bp = Blueprint('intake', __name__, url_prefix='/intake')


@intake_bp.route('/create_semester', methods=['GET', 'POST'])
def create_semester():
    if request.method == 'POST':
        semester_name = request.form.get('semester_name')
        recruitment_started = request.form.get('recruitment_started')
        recruitment_end = request.form.get('recruitment_end')

        semester = Semester(semester_name=semester_name, recruitment_started=recruitment_started, recruitment_end=recruitment_end)
        db.session.add(semester)
        db.session.commit()

        flash('Semester created successfully!')
        return redirect(url_for('home'))

    return render_template('intake/create_semester.html')