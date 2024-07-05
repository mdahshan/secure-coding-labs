from flask import Flask, request, render_template, \
redirect, url_for, g, session

import sqlite3

app = Flask(__name__)
app.secret_key = 'supersecretkey'

DATABASE = 'customer_accounts.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    query = f"SELECT user_id FROM users\
    WHERE username = '{username}' \
    AND password = '{password}'"
    
    db = get_db()
    cur = db.execute(query)
    user = cur.fetchone()

    if user:
        session['user_id'] = user[0]
        return redirect(url_for('account'))
    else:
        return "Invalid username or password"

@app.route('/account')
def account():
    if 'user_id' not in session:
        return redirect(url_for('index'))

    user_id = session['user_id']
    db = get_db()
    cur = db.execute(f"SELECT username FROM users\
    WHERE user_id = {user_id}")
    username = cur.fetchone()

    cur = db.execute(f"SELECT balance FROM accounts\
    WHERE user_id = {user_id}")
    balance = cur.fetchone()

    if username and balance:
        return render_template('balance.html', username=username[0], balance=balance[0])
    else:
        return "Account not found"

if __name__ == '__main__':
    app.run(debug=True)
