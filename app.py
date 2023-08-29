import sqlalchemy
import requests
import subprocess
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask import Flask, request, render_template, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///DetectorMal.db'  # Replace with your MySQL connection details
db = SQLAlchemy(app) # create database 


# Create the user class
class User(db.Model):
    #create table for database
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        print(request.form)
        print(request.form["username"])
        uname = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        # Create a new user instance
        new_user = User(username=uname, email=email, password=password)

        # Add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        flash(f"Account created for {uname}!", 'success')

        # Print user information in the console/terminal
        print(f"New user created: {new_user.username}, {new_user.email}")

        return redirect(url_for('home'))

    return render_template('sign_up.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Query the database for the user
        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            # User found, sign in successful
            print("VALID USER")
            flash(f'Sign in successful for{username}!', 'success')
            return redirect(url_for('home'))
        else:
            print("INVALID USER")
            # User not found or incorrect password, sign in failed
            flash('Invalid username or password! Sign up at the sign up page.', 'error')
            return redirect(url_for('signin'))

    return render_template('sign_in.html')

@app.route('/sandbox')
def sandbox():
    return render_template('sandbox.html')

@app.route('/urlResult', methods = ['POST', 'GET'])
def urlResult():
    url = request.form['name']

    headers = {'accept': 'application/json',
               'user-agent': 'Falcon Sandbox',
               'api-key': 'rr8apy9g30c3065f9evu945q229921c6fe9gl7hxba57df3a6e117h4012e8d257',
               'Content-Type': 'application/x-www-form-urlencoded'}
    data = 'scan_type=all&url=' + url
    response = requests.post('https://www.hybrid-analysis.com/api/v2/quick-scan/url', headers=headers, data=data)
    result = response.json()
    #print(result)

    return render_template("sandbox.html", name=result)

@app.route('/tracert')
def tracert():
    return render_template("tracert.html")

@app.route('/traceResult', methods=['POST', 'GET'])
def traceResult():
    dns = request.form['name']

    dnsOutput = subprocess.run(['tracert', dns], capture_output=True, text=True).stdout
    return render_template('tracert.html', host=dnsOutput)

    
@app.route('/nslookup')
def nslookup():
    return render_template('nslookup.html')

@app.route('/nsResult', methods = ['POST','GET'])
def nsResult():
    url = request.form['name']

    urlOutput = subprocess.run(['nslookup', url], capture_output=True, text=True).stdout
    return render_template('nslookup.html', name=urlOutput)

@app.route('/ping')
def ping():
    return render_template('ping.html')

@app.route('/pingResult', methods = ['POST','GET'])
def pingResult():
    dns = request.form['name']

    dnsOutput = subprocess.run(['ping', dns], capture_output=True, text=True).stdout
    return render_template('ping.html', name=dnsOutput)


@app.route('/')
def home():
    return render_template('home.html')

with app.app_context():
    db.create_all()
    
if __name__ == '__main__':
    app.secret_key = 'secretkey'
    app.run()
