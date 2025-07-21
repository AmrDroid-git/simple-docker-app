from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import time

app = Flask(__name__)

# Wait a bit for MySQL to be ready (can also use healthchecks)
time.sleep(10)

# MySQL DB config (using environment variables is also possible)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:rootpassword@db:3306/flaskdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Model
class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    hobby = db.Column(db.String(100))
    address = db.Column(db.String(200))

# Create the table
with app.app_context():
    db.create_all()

# Routes
@app.route('/')
def index():
    return render_template('index.html')

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

@app.route('/all_persons')
def all_persons():
    persons = Person.query.all()
    return render_template('all_persons.html', persons=persons)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
