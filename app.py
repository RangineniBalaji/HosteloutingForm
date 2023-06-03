from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user_details.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key_here'

db = SQLAlchemy(app)


class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    password = db.Column(db.String(100))
    email = db.Column(db.String(100))

    def __init__(self, email, password):
        self.password = password
        self.email = email


class UserDetails(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100))
    register_number = db.Column(db.String(100))
    room_number = db.Column(db.String(100))
    hostel = db.Column(db.String(100))
    leaving_time = db.Column(db.String(100))
    return_time = db.Column(db.String(100))
    reason = db.Column(db.String(100))

    def __init__(self, user_id, name, register_number, room_number, hostel, leaving_time, return_time, reason):
        self.user_id = user_id
        self.name = name
        self.register_number = register_number
        self.room_number = room_number
        self.hostel = hostel
        self.leaving_time = leaving_time
        self.return_time = return_time
        self.reason = reason


@app.route('/')
def home():
    return render_template('RegisterPage.html')


@app.route('/signup', methods=['POST'])
def signup():
    email = request.form.get('email')
    password = request.form.get('pswd')

    # Check if the user already exists in the database
    with app.app_context():
        user = users.query.filter_by(email=email).first()
        if user:
            return "User already exists"

        # Create a new user and add it to the database
        new_user = users(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

    return "signed Up"


@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('pswd')

    # Verify the user's credentials against the database
    with app.app_context():
        user = users.query.filter_by(email=email, password=password).first()
        if user:
            if email == 'admin@gmail.com' and password == 'admin':
                with app.app_context():
                    user_details = UserDetails.query.all()
                return render_template('adminPage.html', user_details=user_details)
            else:
                session['email'] = email  # Store the email in the session
                return render_template('homePage.html')
        else:
            return "Invalid credentials"


@app.route('/homePage.html')
def homePage():
    return render_template('homePage.html')


@app.route('/submit_details', methods=['POST'])
def submit_details():
    email = session['email']  # Retrieve the email from the session
    user = users.query.filter_by(email=email).first()

    name = request.form.get('name')
    register_number = request.form.get('register_number')
    room_number = request.form.get('room_number')
    hostel = request.form.get('hostel')
    leaving_time = request.form.get('leaving_time')
    return_time = request.form.get('return_time')
    reason = request.form.get('reason')

    new_user_details = UserDetails(user_id=user._id, name=name, register_number=register_number,
                                   room_number=room_number, hostel=hostel, leaving_time=leaving_time,
                                   return_time=return_time, reason=reason)
    db.session.add(new_user_details)
    db.session.commit()

    print(name,register_number,room_number,hostel, leaving_time,return_time, reason)

    return "Details saved successfully"





if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
