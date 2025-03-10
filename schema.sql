-- Users table (both mentors and mentees)
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL,  -- 'mentor' or 'mentee'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Mentor profiles
CREATE TABLE IF NOT EXISTS mentor_profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    full_name TEXT,
    bio TEXT,
    expertise TEXT,
    FOREIGN KEY (user_id) REFERENCES users (id)
);

-- Bookings
CREATE TABLE IF NOT EXISTS bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mentor_id INTEGER,
    mentee_id INTEGER,
    booking_date TEXT,
    status TEXT DEFAULT 'booked',
    FOREIGN KEY (mentor_id) REFERENCES users (id),
    FOREIGN KEY (mentee_id) REFERENCES users (id)
);