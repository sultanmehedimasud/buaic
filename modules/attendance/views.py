from datetime import datetime

from flask import jsonify, redirect, render_template, request, url_for
from flask_login import login_required

from app import db
from modules.event.models import Event
from modules.user.models import User

from . import attendance_bp
from .models import Attendance


@attendance_bp.route('/', methods=['GET', 'POST'])
@login_required
def event_input():
    if request.method == 'POST':
        event_id = request.form.get('event_id')
        return redirect(url_for('attendance.record_attendance', event_id=event_id))

    events = Event.query.filter(Event.end_date > datetime.now()).all()
    return render_template('attendance/event_id_input.html', events=events)


@attendance_bp.route('/record', methods=['GET', 'POST'])
@login_required
def record_attendance():
    if request.method == 'GET':
        all_users = User.query.with_entities(User.student_id, User.rfid, User.name, User.department, User.designation).all()

        serialized_users = [
            {
                'student_id': user.student_id,
                'rfid': user.rfid or 'N/A',
                'name': user.name,
                'department': user.department,
                'designation': user.designation
            }
            for user in all_users
        ]
        
        event_id = request.args.get('event_id')
    return render_template('attendance/attendance.html', users=serialized_users, event_id=event_id)


@attendance_bp.route('/save_attendance', methods=['POST'])
@login_required
def save_attendance():
    if request.method == 'POST':
        attendance_data = request.json
        
        today_date = datetime.now().date()

        for entry in attendance_data['attendanceData']:

            timestamp_time = datetime.strptime(entry['timestamp'], 'Sign In: %I:%M %p').time()
            formatted_timestamp = datetime.combine(today_date, timestamp_time)

            attendance_entry = Attendance(
                student_id=entry['student_id'],
                timestamp=formatted_timestamp,
                event_id=attendance_data['event_id']
            )
            db.session.add(attendance_entry)

        db.session.commit()

        return jsonify({'message': 'Attendance saved successfully!'}), 200