from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash
import os
from datetime import datetime
from models import User, MentorProfile, Booking, init_db, get_db_connection

# Initialize the app
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secure string

# Initialize the database
init_db()

# Check if user is logged in
def is_logged_in():
    return 'user_id' in session

# Get current user
def get_current_user():
    if is_logged_in():
        return User.get_by_id(session['user_id'])
    return None

# Routes
@app.route('/')
def index():
    return render_template('index.html', user=get_current_user())

# Authentication routes
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        
        if User.create_user(username, email, password, role):
            flash('Account created successfully! Please log in.')
            return redirect(url_for('login'))
        else:
            flash('Username or email already exists!')
    
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.get_by_username(username)
        
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            flash('Logged in successfully!')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password!')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Logged out successfully!')
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if not is_logged_in():
        flash('Please log in first!')
        return redirect(url_for('login'))
    
    user = get_current_user()
    
    if user.role == 'mentor':
        profile = MentorProfile.get_by_user_id(user.id)
        bookings = Booking.get_mentor_bookings(user.id)
        return render_template('dashboard.html', user=user, profile=profile, bookings=bookings)
    else:
        bookings = Booking.get_mentee_bookings(user.id)
        return render_template('dashboard.html', user=user, bookings=bookings)

# Mentor profile routes
@app.route('/create_profile', methods=['GET', 'POST'])
def create_profile():
    if not is_logged_in():
        flash('Please log in first!')
        return redirect(url_for('login'))
    
    user = get_current_user()
    
    if user.role != 'mentor':
        flash('Only mentors can create profiles!')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        full_name = request.form['full_name']
        bio = request.form['bio']
        expertise = request.form['expertise']
        
        MentorProfile.create_profile(user.id, full_name, bio, expertise)
        flash('Profile created/updated successfully!')
        return redirect(url_for('dashboard'))
    
    # Check if profile already exists
    profile = MentorProfile.get_by_user_id(user.id)
    
    return render_template('create_profile.html', user=user, profile=profile)

@app.route('/mentor/<int:mentor_id>')
def mentor_profile(mentor_id):
    mentor = User.get_by_id(mentor_id)
    
    if not mentor or mentor.role != 'mentor':
        flash('Mentor not found!')
        return redirect(url_for('marketplace'))
    
    profile = MentorProfile.get_by_user_id(mentor_id)
    
    if not profile:
        flash('Mentor profile not found!')
        return redirect(url_for('marketplace'))
    
    return render_template('mentor_profile.html', mentor=mentor, profile=profile, user=get_current_user())

# Marketplace routes
@app.route('/marketplace')
def marketplace():
    search = request.args.get('search', '')
    
    if search:
        mentors = MentorProfile.search_mentors(search)
    else:
        mentors = MentorProfile.get_all_mentors()
    
    return render_template('marketplace.html', mentors=mentors, search=search, user=get_current_user())

# Booking routes
@app.route('/book/<int:mentor_id>', methods=['GET', 'POST'])
def book_session(mentor_id):
    if not is_logged_in():
        flash('Please log in first!')
        return redirect(url_for('login'))
    
    user = get_current_user()
    
    if user.role != 'mentee':
        flash('Only mentees can book sessions!')
        return redirect(url_for('marketplace'))
    
    mentor = User.get_by_id(mentor_id)
    
    if not mentor or mentor.role != 'mentor':
        flash('Mentor not found!')
        return redirect(url_for('marketplace'))
    
    if request.method == 'POST':
        booking_date = request.form['booking_date']
        
        Booking.create_booking(mentor_id, user.id, booking_date)
        flash('Session booked successfully!')
        return redirect(url_for('dashboard'))
    
    profile = MentorProfile.get_by_user_id(mentor_id)
    
    return render_template('booking.html', mentor=mentor, profile=profile, user=user)

if __name__ == '__main__':
    app.run(debug=True)