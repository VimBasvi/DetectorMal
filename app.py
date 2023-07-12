import git
from flask import Flask, render_template, url_for, flash, redirect, request
from forms import RegistrationForm
from flask_behind_proxy import FlaskBehindProxy
from flask_sqlalchemy import SQLAlchemy
import requests
import subprocess

app = Flask(__name__)
proxied = FlaskBehindProxy(app)
app.config['SECRET_KEY'] = '03cee159f0fe228fa4bbdafc939a23d1'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(20), unique=True, nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  password = db.Column(db.String(60), nullable=False)

  def __repr__(self):
    return f"User('{self.username}', '{self.email}')"

with app.app_context():
  db.create_all()


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit(): # checks if entries are valid
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home')) # if so - send to home page
    return render_template('register.html', title='Register', form=form)

@app.route("/sandbox")
def sandbox():
    return render_template("sandbox.html")

@app.route("/urlResult", methods=['POST', 'GET'])
def urlResult():
    output = request.form.to_dict()
    url = output["url"]

    headers = {'accept': 'application/json',
               'user-agent': 'Falcon Sandbox',
               'api-key': 'rr8apy9g30c3065f9evu945q229921c6fe9gl7hxba57df3a6e117h4012e8d257',
               'Content-Type': 'application/x-www-form-urlencoded'}
    data = 'scan_type=all&url=' + url
    response = requests.post('https://www.hybrid-analysis.com/api/v2/quick-scan/url', headers=headers, data=data)
    urlOutput = response.json()

    return render_template("sandbox.html", urlOutput=urlOutput)

@app.route("/ping")
def ping():
    return render_template("ping.html")

@app.route("/dnsResult", methods=['POST', 'GET'])
def dnsResult():
    output = request.form.to_dict()
    dns = output["dns"]

    dnsOutput = subprocess.run(['ping', dns], capture_output=True, text=True).stdout
    return render_template("ping.html", dnsOutput=dnsOutput)

@app.route("/nslookup")
def nslookup():
    return render_template("nslookup.html")

@app.route("/webInfoResult", methods=['POST', 'GET'])
def webInfoResult():
    output = request.form.to_dict()
    web = output["web"]

    webInfoOut = subprocess.run(['nslookup', web], capture_output=True, text=True).stdout
    return render_template("nslookup.html", webInfoOut=webInfoOut)

@app.route("/tracert")
def tracert():
    return render_template("tracert.html")

@app.route("/routeResult", methods=['POST', 'GET'])
def routeResult():
    output = request.form.to_dict()
    dns = output["dns"]

    dnsRouteOut = subprocess.run(['tracert', dns], capture_output=True, text=True).stdout
    return render_template("tracert.html", dnsRouteOut=dnsRouteOut)

@app.route("/update_server", methods=['POST'])
def webhook():
    if request.method == 'POST':
        repo = git.Repo('/home/FlaskWebProject1/FlaskWebProject1')
        origin = repo.remotes.origin
        origin.pull()
        return 'Updated PythonAnywhere successfully', 200
    else:
        return 'Wrong event type', 400

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
