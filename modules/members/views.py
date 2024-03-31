from flask import Blueprint, render_template

from app import db
from modules.user.models import User

members_bp = Blueprint('members', __name__, url_prefix='/members')

@members_bp.route('/all-members')
def all_members():
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
def user_profile(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('members/member_details.html', user=user)