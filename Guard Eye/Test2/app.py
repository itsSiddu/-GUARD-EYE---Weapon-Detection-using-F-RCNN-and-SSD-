from flask import Flask, request

app = Flask(__name__)
@app.route('/input', methods=['POST'])
def handle_input():
    data = request.get_json()
    # Do something with the data, e.g. print it to the console
    print(data)
    return 'OK'
