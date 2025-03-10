import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash

# Database initialization
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    if not os.path.exists('database.db'):
        conn = get_db_connection()
        with open('schema.sql') as f:
            conn.executescript(f.read())
        conn.commit()
        conn.close()

# User model
class User:
    def __init__(self, id=None, username=None, email=None, password=None, role=None):
        self.id = id
        self.username = username
        self.email = email
        self.password = password
        self.role = role
        self.is_authenticated = False
        self.is_active = True
        self.is_anonymous = False

    def get_id(self):
        return str(self.id)

    @staticmethod
    def get_by_id(user_id):
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
        conn.close()
        
        if user:
            user_obj = User(
                id=user['id'],
                username=user['username'],
                email=user['email'],
                password=user['password'],
                role=user['role']
            )
            user_obj.is_authenticated = True
            return user_obj
        return None

    @staticmethod
    def get_by_username(username):
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()
        
        if user:
            user_obj = User(
                id=user['id'],
                username=user['username'],
                email=user['email'],
                password=user['password'],
                role=user['role']
            )
            return user_obj
        return None

    @staticmethod
    def create_user(username, email, password, role):
        hashed_password = generate_password_hash(password)
        
        conn = get_db_connection()
        try:
            conn.execute(
                'INSERT INTO users (username, email, password, role) VALUES (?, ?, ?, ?)',
                (username, email, hashed_password, role)
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            # Username or email already exists
            return False
        finally:
            conn.close()

    def check_password(self, password):
        return check_password_hash(self.password, password)

# Mentor Profile model
class MentorProfile:
    @staticmethod
    def get_by_user_id(user_id):
        conn = get_db_connection()
        profile = conn.execute('SELECT * FROM mentor_profiles WHERE user_id = ?', (user_id,)).fetchone()
        conn.close()
        return profile

    @staticmethod
    def create_profile(user_id, full_name, bio, expertise):
        conn = get_db_connection()
        
        # Check if profile already exists
        existing = conn.execute('SELECT * FROM mentor_profiles WHERE user_id = ?', (user_id,)).fetchone()
        
        if existing:
            # Update existing profile
            conn.execute(
                'UPDATE mentor_profiles SET full_name = ?, bio = ?, expertise = ? WHERE user_id = ?',
                (full_name, bio, expertise, user_id)
            )
        else:
            # Create new profile
            conn.execute(
                'INSERT INTO mentor_profiles (user_id, full_name, bio, expertise) VALUES (?, ?, ?, ?)',
                (user_id, full_name, bio, expertise)
            )
            
        conn.commit()
        conn.close()
        return True

    @staticmethod
    def get_all_mentors():
        conn = get_db_connection()
        query = '''
        SELECT users.id, users.username, users.email, mentor_profiles.*
        FROM users
        JOIN mentor_profiles ON users.id = mentor_profiles.user_id
        WHERE users.role = 'mentor'
        '''
        mentors = conn.execute(query).fetchall()
        conn.close()
        return mentors

    @staticmethod
    def search_mentors(name):
        conn = get_db_connection()
        query = '''
        SELECT users.id, users.username, users.email, mentor_profiles.*
        FROM users
        JOIN mentor_profiles ON users.id = mentor_profiles.user_id
        WHERE users.role = 'mentor' AND mentor_profiles.full_name LIKE ?
        '''
        mentors = conn.execute(query, (f'%{name}%',)).fetchall()
        conn.close()
        return mentors

# Booking model
class Booking:
    @staticmethod
    def create_booking(mentor_id, mentee_id, booking_date):
        conn = get_db_connection()
        conn.execute(
            'INSERT INTO bookings (mentor_id, mentee_id, booking_date) VALUES (?, ?, ?)',
            (mentor_id, mentee_id, booking_date)
        )
        conn.commit()
        conn.close()
        return True

    @staticmethod
    def get_mentee_bookings(mentee_id):
        conn = get_db_connection()
        query = '''
        SELECT b.*, u.username as mentor_name, mp.full_name as mentor_full_name
        FROM bookings b
        JOIN users u ON b.mentor_id = u.id
        JOIN mentor_profiles mp ON u.id = mp.user_id
        WHERE b.mentee_id = ?
        '''
        bookings = conn.execute(query, (mentee_id,)).fetchall()
        conn.close()
        return bookings

    @staticmethod
    def get_mentor_bookings(mentor_id):
        conn = get_db_connection()
        query = '''
        SELECT b.*, u.username as mentee_name
        FROM bookings b
        JOIN users u ON b.mentee_id = u.id
        WHERE b.mentor_id = ?
        '''
        bookings = conn.execute(query, (mentor_id,)).fetchall()
        conn.close()
        return bookings