from flask import Flask, render_template, request, redirect
import requests

app = Flask(__name__)

@app.route('/')
def form():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    data = {
        'name': request.form['name'],
        'age': request.form['age'],
        'hobby': request.form['hobby'],
        'address': request.form['address']
    }

    try:
        # Post to Server A by service name "server_a"
        res = requests.post('http://server_a:5000/submit', data=data)
        return res.text, res.status_code
    except Exception as e:
        return f"Failed to send data to server A: {e}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
