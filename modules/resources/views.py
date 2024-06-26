from datetime import datetime

from flask import abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from . import resource_bp
from .models import Booking, Room, db


# Automatically remove all bookings that have expired and mark the rooms as available
@resource_bp.before_request
def remove_expired_bookings():
    bookings = Booking.query.all()
    for booking in bookings:
        if booking.end_time < datetime.now():
            room = Room.query.get(booking.room_id)
            room.booked = False
            db.session.delete(booking)
            db.session.commit()


@resource_bp.route('/resources/add_room', methods=['GET', 'POST'])
@login_required
def add_room():
    if current_user.designation not in ['Governing Body', 'President', 'Vice President', 'Secretary', 'Treasurer', 'Director', 'Assistant Director']:
        abort(403)
        
    if request.method == 'POST':
        room_number = request.form.get('room_number')
        if Room.query.filter_by(room_number=room_number).first():
            flash('A room with this number already exists!', 'danger')
        else:
            try:
                new_room = Room(room_number=room_number, booked=False)
                db.session.add(new_room)
                db.session.commit()
                flash('Room added successfully!', 'success')
                return redirect(url_for('resources.add_room'))
            except Exception as e:
                flash('An error occurred while adding the room: {}'.format(e), 'danger')
    return render_template('resources/add_room.html')


@resource_bp.route('/resources/rooms', methods=['GET', 'POST'])
@login_required
def rooms():
    if current_user.designation not in ['Governing Body', 'President', 'Vice President', 'Secretary', 'Treasurer', 'Director', 'Assistant Director']:
        abort(403)
        
    rooms = Room.query.all()
    return render_template('resources/rooms.html', rooms=rooms)


@resource_bp.route('/resources/edit_room/<int:room_id>', methods=['GET', 'POST'])
@login_required
def edit_room(room_id):
    
    if current_user.designation not in ['Governing Body', 'President', 'Vice President', 'Secretary', 'Treasurer', 'Director', 'Assistant Director']:
        abort(403)
    
    room = Room.query.get(room_id)
    
    if not room:
        flash('Room not found!', 'danger')
        return redirect(url_for('resources.rooms'))

    if request.method == 'POST':
        new_room_number = request.form.get('room_number')
        if Room.query.filter(Room.id != room_id, Room.room_number == new_room_number).first():
            flash('A room with this number already exists!', 'danger')
        else:
            room.room_number = new_room_number
            db.session.commit()
            flash('Room updated successfully!', 'success')
            return redirect(url_for('resources.rooms'))
    else:
        return render_template('resources/edit_room.html', room=room)
    
@resource_bp.route('/resources/delete_room/<int:room_id>', methods=['GET', 'POST'])
@login_required
def delete_room(room_id):
    if current_user.designation not in ['Governing Body', 'President', 'Vice President', 'Secretary', 'Treasurer', 'Director', 'Assistant Director']:
        abort(403)
        
    room = Room.query.get(room_id)
    Booking.query.filter_by(room_id=room_id).delete()
    
    for booking in Booking.query.filter_by(room_id=room_id).all():
        db.session.delete(booking)
        
    if not room:
        flash('Room not found!', 'danger')
    else:
        db.session.delete(room)
        db.session.commit()
        flash('Room deleted successfully!', 'success')
        
    return redirect(url_for('resources.rooms'))


@resource_bp.route('/resources/book_room', methods=['GET'])
@login_required
def book_room():
    if request.method == 'GET':
        available_rooms = Room.query.filter_by(booked=False).all()
        return render_template('resources/book_room.html', rooms=available_rooms)

@resource_bp.route('/resources/booking', methods=['POST'])
@login_required
def booking():
    if request.method == 'POST':
        room_id = request.form.get('room-id')
        start_time = datetime.strptime(request.form.get('start-time'), '%Y-%m-%dT%H:%M')
        end_time = datetime.strptime(request.form.get('end-time'), '%Y-%m-%dT%H:%M')

        if start_time >= end_time:
            flash('Invalid booking time!', 'danger')
        else:
            booking = Booking(room_id=room_id, booked_by=current_user.id, start_time=start_time, end_time=end_time)
            db.session.add(booking)
            room = Room.query.get(room_id)
            room.booked = True
            db.session.commit()
            flash('Room booked successfully!', 'success')
    
    return redirect(url_for('resources.book_room'))

@resource_bp.route('/resources/my_bookings')
@login_required
def my_bookings():
    my_bookings = Booking.query.filter_by(booked_by=current_user.id).all()
    rooms = Room.query.all()
    rooms = {room.id: room.room_number for room in rooms}
    return render_template('resources/my_bookings.html', my_bookings=my_bookings, rooms = rooms)

@resource_bp.route('/resources/cancel_booking/<int:booking_id>', methods=['POST'])
@login_required
def cancel_booking(booking_id):
    if request.method == 'POST':
        booking = Booking.query.get(booking_id)
        room = Room.query.get(booking.room_id)
        db.session.delete(booking)
        room.booked = False
        db.session.commit()
        flash('Booking canceled successfully!', 'success')
        
    return redirect(url_for('resources.my_bookings'))