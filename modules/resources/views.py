from datetime import datetime

from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user

from . import resource_bp
from .models import Booking, Room, db


@resource_bp.route('/resources/add_room', methods=['GET', 'POST'])
def add_room():
    if request.method == 'POST':
        room_number = request.form.get('room_number')
        if Room.query.filter_by(room_number=room_number).first():
            flash('A room with this number already exists!', 'error')
        else:
            try:
                new_room = Room(room_number=room_number, booked=False)
                db.session.add(new_room)
                db.session.commit()
                flash('Room added successfully!', 'success')
                return redirect(url_for('resources.add_room'))
            except Exception as e:
                flash('An error occurred while adding the room: {}'.format(e), 'error')
    return render_template('resources/add_room.html')

@resource_bp.route('/resources/rooms', methods=['GET', 'POST'])
def rooms():
    rooms = Room.query.all()
    return render_template('resources/rooms.html', rooms=rooms)

@resource_bp.route('/resources/edit_room/<int:room_id>', methods=['GET', 'POST'])
def edit_room(room_id):
    
    room = Room.query.get(room_id)
    
    if not room:
        flash('Room not found!', 'error')
        return redirect(url_for('resources.rooms'))

    if request.method == 'POST':
        new_room_number = request.form.get('room_number')
        if Room.query.filter(Room.id != room_id, Room.room_number == new_room_number).first():
            flash('A room with this number already exists!', 'error')
        else:
            room.room_number = new_room_number
            db.session.commit()
            flash('Room updated successfully!', 'success')
            return redirect(url_for('resources.rooms'))
    else:
        return render_template('resources/edit_room.html', room=room)
    
@resource_bp.route('/resources/delete_room/<int:room_id>', methods=['GET', 'POST'])
def delete_room(room_id):
    room = Room.query.get(room_id)
    if not room:
        flash('Room not found!', 'error')
    else:
        db.session.delete(room)
        db.session.commit()
        flash('Room deleted successfully!', 'success')
        
    return redirect(url_for('resources.rooms'))


@resource_bp.route('/resources/book_room', methods=['GET'])
def book_room():
    if request.method == 'GET':
        available_rooms = Room.query.filter_by(booked=False).all()
        return render_template('resources/book_room.html', rooms=available_rooms)

@resource_bp.route('/resources/booking', methods=['POST'])
def booking():
    if request.method == 'POST':
        room_id = request.form.get('room')
        print(request.form)
        start_time = datetime.strptime(request.form.get('start-time'), '%Y-%m-%dT%H:%M')
        end_time = datetime.strptime(request.form.get('end-time'), '%Y-%m-%dT%H:%M')

        if start_time >= end_time:
            flash('Invalid booking time!', 'error')
        else:
            booking = Booking(room_id=room_id, booked_by=current_user.id, start_time=start_time, end_time=end_time)
            db.session.add(booking)
            room = Room.query.get(room_id)
            room.booked = True
            db.session.commit()
            flash('Room booked successfully!', 'success')
    
    return redirect(url_for('resources.book_room'))

@resource_bp.route('/resources/my_bookings')
def my_bookings():
    my_bookings = Booking.query.filter_by(booked_by=current_user.id).all()
    return render_template('resources/my_bookings.html', my_bookings=my_bookings)

@resource_bp.route('/resources/cancel_booking/<int:booking_id>', methods=['POST'])
def cancel_booking(booking_id):
    if request.method == 'POST':
        booking = Booking.query.get(booking_id)
        room = Room.query.get(booking.room_id)
        db.session.delete(booking)
        room.booked = False
        db.session.commit()
        flash('Booking canceled successfully!', 'success')
        
    return redirect(url_for('resources/my_bookings'))