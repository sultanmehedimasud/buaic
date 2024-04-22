from datetime import datetime

from flask import (Blueprint, abort, flash, redirect, render_template, request,
                   session, url_for)
from flask_login import current_user, login_manager, login_required

from app import db, login_manager

from . import polls_bp
from .models import Polls, Voted


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@polls_bp.route('/polls/create_poll', methods=['GET', 'POST'])
@login_required
def create_poll():
    if current_user.designation not in ['Governing Body', 'President', 'Vice President', 'Secretary', 'Treasurer', 'Director', 'Assistant Director']:
        abort(403)
    if request.method == 'POST':
        question = request.form.get('question')
        option1 = request.form.get('option1')
        option2 = request.form.get('option2')
        option3 = request.form.get('option3')
        option4 = request.form.get('option4')
        
        if not option1 or not option2:
            flash('Options 1 and 2 are required.', 'danger')
            return redirect(url_for('polls.create_poll'))

        poll = Polls(question=question, option1=option1, option2=option2, option3=option3, option4=option4)
        db.session.add(poll)
        db.session.commit()
        
        flash('Poll created successfully!', 'success')
        return redirect(url_for('polls.view_polls'))
    
    return render_template('polls/create_poll.html')


@polls_bp.route('/polls/view_polls')
@login_required
def view_polls():
    polls = Polls.query.all()
    polls_dict = {}

    for poll in polls:
        polls_dict[poll.id] = {'option1': poll.option1,
                               'option2': poll.option2,
                                'option3': poll.option3,
                                'option4': poll.option4,
                                'count_option1': poll.count_option1,
                                'count_option2': poll.count_option2,
                                'count_option3': poll.count_option3,
                                'count_option4': poll.count_option4
                               }
            
    
    return render_template('polls/view_polls.html', polls=polls, json_polls=polls_dict)


@polls_bp.route('/polls/vote/<int:poll_id>', methods=['GET', 'POST'])
@login_required
def vote(poll_id):
    poll = Polls.query.get(poll_id)
    question = poll.question
    options = [poll.option1, poll.option2, poll.option3, poll.option4]
    user_voted = Voted.query.filter_by(poll_id=poll_id, user_id=current_user.id).first()
    
    if request.method == 'POST' and not user_voted:

        option = request.form.get('option')
        
        if option == options[0]:
            poll.count_option1 += 1
            
        elif option == options[1]:
            poll.count_option2 += 1
            
        elif option == options[2]:
            poll.count_option3 += 1
            
        elif option == options[3]:
            poll.count_option4 += 1
             
        voted = Voted(poll_id=poll_id, user_id=current_user.id)

        db.session.add(voted)
        
        db.session.commit()
        
        flash('Voted successfully!', 'success')
        return redirect(url_for('polls.view_polls'))
    
    if user_voted:
            flash('You have already voted!', 'danger')
            return redirect(url_for('polls.view_polls'))
        
    return render_template('polls/vote.html', poll=poll, question=question, options=options, user_voted=user_voted)


@polls_bp.route('/polls/delete_poll/<int:poll_id>')
@login_required
def delete_poll(poll_id):
    if current_user.designation not in ['Governing Body', 'President', 'Vice President', 'Secretary', 'Treasurer', 'Director', 'Assistant Director']:
        abort(403)
    poll = Polls.query.get(poll_id)
    voted = Voted.query.filter_by(poll_id=poll_id).all()

    for vote in voted:
        db.session.delete(vote)
    
    db.session.commit()
    db.session.delete(poll)
    db.session.commit()
    
    flash('Poll deleted successfully!', 'success')
    return redirect(url_for('polls.view_polls'))