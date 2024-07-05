from flask import Flask, request, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta
import os
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Read secret key from environment variable
app.secret_key = os.getenv('FLASK_SECRET_KEY') 

app.config.update(
    SESSION_COOKIE_SECURE=True,  # Ensure cookies are only sent over HTTPS
    SESSION_COOKIE_SAMESITE='Lax',  # Protect against CSRF
    PERMANENT_SESSION_LIFETIME=timedelta(minutes=1)  # Set session timeout
)

# Load users from JSON file in the same directory as this script
def load_users():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    users_path = os.path.join(base_dir, 'users.json')
    with open(users_path, 'r') as f:
        return json.load(f)

users = load_users()

@app.route('/')
def home():
    return '''
        <h1>Welcome!</h1>
        <p><a href="/login">Login</a></p>
        <p><a href="/admin">Admin Page</a></p>
        <p><a href="/logout">Logout</a></p>
    '''

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and check_password_hash(users[username], password):
            session['username'] = username
            session.permanent = True  # Use permanent sessions to enable timeout
            return redirect(url_for('home'))
        return 'Invalid credentials!'
    return '''
        <form method="post">
            Username: <input type="text" name="username"><br>
            Password: <input type="password" name="password"><br>
            <input type="submit" value="Login">
        </form>
    '''

@app.route('/admin')
def admin():
    if 'username' in session and session['username'] == 'admin':
        return '<h1>Welcome to the admin page, admin!</h1>'
    return 'You are not authorised to view this page!'

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
