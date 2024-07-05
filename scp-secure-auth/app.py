from flask import Flask, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# User database
users = {
    'user': 'password',
    'admin': 'adminpass'
}

@app.route('/')
def home():
    return '''
        <h1>Welcome!</h1>
        <p><a href="/login">Login</a></p>
        <p><a href="/admin">Admin Page</a></p>
    '''

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['username'] = username
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

if __name__ == '__main__':
    app.run(debug=True)
