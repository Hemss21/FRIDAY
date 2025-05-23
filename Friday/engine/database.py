import sqlite3
import os
import re


DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)),'data', 'login.db')

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_password(password):
    if not 8 <= len(password) <= 16:
        return False
    if not re.search(r'[A-Z]', password):  # Capital letter
        return False
    if not re.search(r'[a-z]', password):  # Small letter
        return False
    if not re.search(r'\d', password):     # Number
        return False
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):  # Symbol
        return False
    return True

def verify_login(username, password):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('SELECT id, first_name FROM users WHERE username=? AND password=?', (username, password))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                "status": True, 
                "message": "Login successful",
                "user_id": result[0],
                "first_name": result[1]
            }
        return {"status": False, "message": "Invalid email or password"}
    except Exception as e:
        return {"status": False, "message": "An error occurred during login"}

def get_current_user():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        # Get the currently logged in user's information
        cursor.execute('SELECT first_name FROM users WHERE id = ?', (current_user_id,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {"status": True, "first_name": result[0]}
        return {"status": False, "first_name": ""}
    except Exception as e:
        return {"status": False, "first_name": "", "error": str(e)}

def create_user(first_name, last_name, username, password):
    validation_errors = {
        "username": "",
        "password": ""
    }
    
    # Validate inputs
    if not validate_email(username):
        validation_errors["username"] = "Invalid email format"
    
    if not validate_password(password):
        validation_errors["password"] = "Password must contain:\n- 8-16 characters\n- One capital letter\n- One small letter\n- One numerical\n- One special symbol"
    
    if validation_errors["username"] or validation_errors["password"]:
        return {"status": False, "errors": validation_errors}
    
    try:
        # Ensure database exists
        init_database()
        
        # Create connection and insert user
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Check if email exists
        cursor.execute('SELECT username FROM users WHERE username = ?', (username,))
        if cursor.fetchone():
            validation_errors["username"] = "Email already exists"
            return {"status": False, "errors": validation_errors}
        
        # Insert new user
        cursor.execute('''
            INSERT INTO users (first_name, last_name, username, password) 
            VALUES (?, ?, ?, ?)
        ''', (first_name, last_name, username, password))
        
        conn.commit()
        return {"status": True, "errors": validation_errors}
        
    except sqlite3.IntegrityError:
        validation_errors["username"] = "Email already exists"
        return {"status": False, "errors": validation_errors}
    except Exception as e:
        print(f"Database error: {str(e)}")  # For debugging
        return {"status": False, "errors": {"username": "Failed to create account", "password": ""}}
    finally:
        if 'conn' in locals():
            conn.close()

def init_database():
    # Create data directory if it doesn't exist
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_google_user BOOLEAN DEFAULT 0
        )
    ''')
    
    conn.commit()
    conn.close()

def create_google_user(email, first_name, last_name):
    try:
        init_database()
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Check if email exists
        cursor.execute('SELECT email FROM google_account WHERE email = ?', (email,))
        user = cursor.fetchone()
        
        if user:
            # Update existing user
            cursor.execute('''
                UPDATE google_account 
                SET first_name = ?, last_name = ?
                WHERE email = ?
            ''', (first_name, last_name, email))
        else:
            # Insert new Google user
            cursor.execute('''
                INSERT INTO google_account (email, first_name, last_name) 
                VALUES (?, ?, ?)
            ''', (email, first_name, last_name))
        
        conn.commit()
        
        # Get user information for session
        cursor.execute('SELECT id, first_name FROM google_account WHERE email = ?', (email,))
        result = cursor.fetchone()
        
        return {
            "status": True,
            "user_id": result[0],
            "first_name": result[1]
        }
        
    except Exception as e:
        print(f"Database error: {str(e)}")  # For debugging
        return {"status": False, "message": "Failed to create/update Google user"}
    finally:
        if 'conn' in locals():
            conn.close()

def check_session():
    # You can implement more sophisticated session checking here
    # For now, we'll return a simple response
    try:
        return {"status": True}
    except Exception as e:
        return {"status": False, "message": str(e)}
