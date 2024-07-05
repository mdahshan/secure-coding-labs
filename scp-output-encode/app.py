from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def home():
    return '''
        <h1>Enter some text:</h1>
        <form action="/display" method="post">
            <input size="50" type="text" 
             name="user_input">
            <input type="submit" value="Submit">
        </form>
    '''

@app.route('/display', methods=['POST'])
def display():
    user_input = request.form['user_input']
    return f'<h1>User Input: {user_input}</h1>'

if __name__ == '__main__':
    app.run(debug=True)
