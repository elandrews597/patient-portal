CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'patient'
);

CREATE TABLE IF NOT EXISTS patients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    full_name TEXT NOT NULL,
    date_of_birth TEXT NOT NULL,
    diagnosis TEXT NOT NULL,
    notes TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id)
);
