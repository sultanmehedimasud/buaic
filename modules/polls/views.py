from datetime import datetime

from flask import (Blueprint, flash, redirect, render_template, request,
                   session, url_for)
from flask_bcrypt import Bcrypt
from flask_login import (LoginManager, current_user, login_manager,
                         login_required, login_user, logout_user)

# from app import db, login_manager
from extensions import db, login_manager
from modules.intake.models import Semester
from modules.user.models import User
from flask import request

from . models import Polls

polls_bp = Blueprint('polls', __name__, url_prefix='/polls')

bcrypt = Bcrypt()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@polls_bp.route('/create_poll', methods=['GET', 'POST'])
@login_required
def create_poll():
    if request.method == 'POST':
        question = request.form.get('question')
        option1 = request.form.get('option1')
        option2 = request.form.get('option2')
        option3 = request.form.get('option3')
        option4 = request.form.get('option4')
        
        #option1 and option2 are required
        if not option1 or not option2:
            flash('Options 1 and 2 are required.', 'danger')
            return redirect(url_for('polls.create_poll'))

        poll = Polls(question=question, option1=option1, option2=option2, option3=option3, option4=option4)
        db.session.add(poll)
        db.session.commit()
        
        flash('Poll created successfully.', 'success')
        return redirect(url_for('polls.view_polls'))
    
    return render_template('polls/create_poll.html')

@polls_bp.route('/view_polls')
@login_required
def view_polls():
    polls = Polls.query.all()
    
    return render_template('polls/view_polls.html', polls=polls)

@polls_bp.route('/vote/<int:poll_id>', methods=['GET', 'POST'])
@login_required
def vote(poll_id):
    poll = Polls.query.get(poll_id)
    question = poll.question
    options = [poll.option1, poll.option2, poll.option3, poll.option4]
    if request.method == 'POST':
        option = request.form.get('option')
        
        if option == options[0]:
            poll.count_option1 += 1
        elif option == options[1]:
            poll.count_option2 += 1
        elif option == options[2]:
            poll.count_option3 += 1
        elif option == options[3]:
            poll.count_option4 += 1
        
        db.session.commit()
        
        flash('Voted successfully.', 'success')
        return redirect(url_for('polls.view_polls'))
    
    return render_template('polls/vote.html',poll=poll, question=question, options=options)

@polls_bp.route('/poll_result/<int:poll_id>')
@login_required
def poll_result(poll_id):
    poll = Polls.query.get(poll_id)
    options = [poll.option1, poll.option2, poll.option3, poll.option4]
    votes = {poll.option1: poll.count_option1, poll.option2: poll.count_option2, poll.option3: poll.count_option3, poll.option4: poll.count_option4}
    majority = max(votes, key=votes.get)

    return render_template('polls/poll_result.html', poll=poll, majority=majority, options=options, votes=votes)

@polls_bp.route('/delete_poll/<int:poll_id>')
@login_required
def delete_poll(poll_id):
    poll = Polls.query.get(poll_id)
    db.session.delete(poll)
    db.session.commit()
    
    flash('Poll deleted successfully.', 'success')
    return redirect(url_for('polls.view_polls'))