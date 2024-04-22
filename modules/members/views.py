import csv
from datetime import datetime

from flask import Blueprint, Response, abort, flash, render_template
from flask_login import current_user, login_required

from app import db
from modules.user.models import User

members_bp = Blueprint('members', __name__, url_prefix='/members')

@members_bp.route('/all-members')
@login_required
def all_members():
    if current_user.designation not in ['Governing Body', 'President', 'Vice President', 'Secretary', 'Treasurer', 'Director', 'Assistant Director']:
        abort(403)
    members = User.query.all()
    
    department_order = [
        'Communication and Marketing',
        'Creative',
        'Event Management',
        'Finance',
        'Human Resources',
        'Press Release and Publications',
        'Research and Development'
    ]
    
    position_order = [
        'Governing Body Members',
        'Director',
        'Assistant Director',
        'Senior Executive',
        'Executive',
        'General Member'
    ]
    
    members_sorted = sorted(members, key=lambda x: (department_order.index(x.department if x.department != 'Governing Body Members' else ''), position_order.index(x.designation)))
    
    return render_template('members/all_members.html', members=members_sorted)


@members_bp.route('/member/<int:user_id>')
@login_required
def user_profile(user_id):
    if current_user.designation not in ['Governing Body', 'President', 'Vice President', 'Secretary', 'Treasurer', 'Director', 'Assistant Director']:
        abort(403)
    user = User.query.get_or_404(user_id)
    return render_template('members/member_details.html', user=user)


@members_bp.route('/export_csv')
@login_required
def export_csv():
    if current_user.designation not in ['Governing Body', 'President', 'Vice President', 'Secretary', 'Treasurer', 'Director', 'Assistant Director']:
        abort(403)
    members = User.query.all()
    with open('members.csv', mode='w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Student ID','Name', 'Email', 'Phone', 'Department', 'Designation'])
        for member in members:
            writer.writerow([member.student_id, member.name, member.email, member.phone, member.department, member.designation])
    
    flash('Excel file has been exported successfully!', 'success')
    return Response(open('members.csv', 'r'), mimetype='text/csv', headers={"Content-disposition":"attachment; filename=members.csv"})