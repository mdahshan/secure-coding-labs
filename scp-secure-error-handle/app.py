from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <h1>Division Calculator</h1>
    <form method="GET" action="/divide">
        <input type="text" name="dividend" 
         placeholder="Dividend" required>
        <input type="text" name="divisor" 
         placeholder="Divisor" required>
        <button type="submit">Divide</button>
    </form>
    '''

@app.route('/divide', methods=['GET'])
def divide():
    dividend = int(request.args.get('dividend'))
    divisor = int(request.args.get('divisor'))
    result = dividend / divisor
    return f'''
    <h1>Result</h1>
    <p>{dividend} / {divisor} = {result}</p>
    '''


if __name__ == '__main__':
    app.run(debug=True)
