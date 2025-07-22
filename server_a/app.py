from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import time

app = Flask(__name__)

# Wait to ensure MySQL is ready
time.sleep(10)

# MySQL database config: service name "db" from docker-compose
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:rootpassword@db:3306/flaskdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize DB
db = SQLAlchemy(app)

# Define the Person model
class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    hobby = db.Column(db.String(100))
    address = db.Column(db.String(200))

# Create table
with app.app_context():
    db.create_all()

# Route: show form
@app.route('/')
def index():
    return render_template('index.html')

# Route: receive form submission (from local or external)
@app.route('/submit', methods=['POST'])
def submit():
    try:
        person = Person(
            name=request.form['name'],
            age=request.form['age'],
            hobby=request.form['hobby'],
            address=request.form['address']
        )
        db.session.add(person)
        db.session.commit()
        return render_template('result.html', **request.form)
    except Exception as e:
        return f"Error submitting data: {e}", 500

# Route: list all stored persons
@app.route('/all_persons')
def all_persons():
    persons = Person.query.all()
    return render_template('all_persons.html', persons=persons)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
