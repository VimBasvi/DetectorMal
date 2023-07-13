import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask import Flask, request, render_template, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///DetectorMAL.db'
db = SQLAlchemy(app)

# create the user class
class User(db.Model):
    __tablename__ = "Users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
@app.route('/', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        # Create a new user instance
        new_user = User(username=username, email=email, password=password)

        # Add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        flash(f"Account created for {username}!", 'success')

        return redirect(url_for('home'))

    return render_template('sign_up.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Query the database for the user
        user = User.query.filter_by(username=username, password=password).first()

        if user:
            # User found, sign in successful
            flash('Sign in successful!', 'success')
            return redirect(url_for('home'))
        else:
            # User not found or incorrect password, sign in failed
            flash('Invalid username or password!', 'error')
            return redirect(url_for('signin'))

    return render_template('sign_in.html')

@app.route('/home')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.secret_key = 'secretkey'
    app.run()
