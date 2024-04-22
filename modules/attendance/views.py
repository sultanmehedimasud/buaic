from datetime import datetime

from flask import (abort, flash, jsonify, redirect, render_template, request,
                   url_for)
from flask_login import current_user, login_required

from app import db
from modules.event.models import Event
from modules.user.models import User

from . import attendance_bp
from .models import Attendance


@attendance_bp.route('/record', methods=['GET', 'POST'])
@login_required
def record_attendance():
    if request.method == 'GET':
        if current_user.designation not in ['Governing Body', 'President', 'Vice President', 'Secretary', 'Treasurer', 'Director', 'Assistant Director']:
            abort(403)
        
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


@attendance_bp.route('/save_attendance', methods=['POST', 'GET'])
@login_required
def save_attendance():
    if current_user.designation not in ['Governing Body', 'President', 'Vice President', 'Secretary', 'Treasurer', 'Director', 'Assistant Director']:
            abort(403)
            
    if request.method == 'POST':
        attendance_data = request.json
        
        today_date = datetime.now().date()

        attendance = Attendance.query.filter_by(event_id=attendance_data['event_id']).all()
                
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

        return url_for('event.list')