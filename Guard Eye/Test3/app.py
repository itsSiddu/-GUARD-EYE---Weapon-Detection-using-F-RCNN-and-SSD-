from flask import Flask, request

app = Flask(__name__)

@app.route('/localhost:8000/hello', methods=['POST'])
def hello():
    data = request.get_json()
    message = 'Hello ' + data['input']
    return {'output': message}

