from flask import Flask, request
import logging
import os

app = Flask(__name__)

# Configure logging
base_dir = os.path.dirname(os.path.abspath(__file__))
log_path = f'{base_dir}/logs'

if not os.path.exists(log_path):
    os.makedirs(log_path)

logging.basicConfig(filename=f'{log_path}/app.log', 
                    level=logging.ERROR)

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

@app.route('/divide')
def divide():
    try:
        dividend = int(request.args.get('dividend'))
        divisor = int(request.args.get('divisor'))
        result = dividend / divisor
        return f'''
        <h1>Result</h1>
        <p>{dividend} / {divisor} = {result}</p>
        '''

    except ZeroDivisionError:
        logging.error('Attempted to divide by zero', exc_info=True)
        return '<h1>Error</h1><p>Cannot divide by zero</p>', 400
    except ValueError:
        logging.error('Invalid input for division', exc_info=True)
        return '<h1>Error</h1><p>Invalid input</p>', 400
    except Exception as e:
        logging.error('An error occurred', exc_info=True)
        return '<h1>Error</h1><p>An internal error occurred</p>', 500

if __name__ == '__main__':
    app.run(debug=False)
