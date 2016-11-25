import os
import sqlite3
import uuid
import hashlib
from flask import Flask, redirect, url_for, request, render_template, session
from functools import wraps

app = Flask(__name__)
app.secret_key = os.urandom(24)

DATABASE = 'database.db'

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


# Adapted from http://flask.pocoo.org/docs/0.11/patterns/viewdecorators/
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            if session['user'] is None:
                return redirect(url_for('login', next=request.url))
            return f(*args, **kwargs)
        except KeyError:
            return redirect(url_for('login', next=request.url))
    return decorated_function


# Adapted from http://flask.pocoo.org/docs/0.11/patterns/viewdecorators/
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.admin is None:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


# Adapted from http://pythoncentral.io/hashing-strings-with-python/
def hash_password(password):
    # uuid is used to generate a random number
    salt = uuid.uuid4().hex
    return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' \
           + salt


# Adapted from http://pythoncentral.io/hashing-strings-with-python/
def hashed_password(hashed_password, user_password):
    password, salt = hashed_password.split(':')
    return hashlib.sha256(salt.encode() + user_password.encode()).hexdigest() \
           + ":" + salt


@app.route("/Login")
def login():
    return render_template('login/login.html', msg='')


@app.route("/CheckLogin", methods=['POST'])
def checkLogin():
    print("Processing data")
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()
        cur.execute("SELECT Password FROM Accounts WHERE Username=?",
                    (username,))
        actual_password = cur.fetchall()
        actual_password = actual_password[0][0]
        if actual_password != "":
            password = hashed_password(actual_password, password)
            cur.execute("SELECT * FROM Accounts WHERE Username=? AND Password=?",
                        (username, password))
            outcome = cur.fetchall()
            if len(outcome) > 0:
                session['user'] = username
                return "/Client"
            else:
                return "/Login"


@app.route("/Logout")
def logout():
    session['user'] = None
    session['admin'] = None
    return redirect(url_for('login'))

@app.route("/HealthData", methods=['POST'])
def HealthData():
    GoodHealth = request.form.get('GoodHealth', default="Error")
    Smoker = request.form.get('Smoker', default="Error")
    SmokeADay = request.form.get('SmokeADay', default="Error")
    Drinker = request.form.get('Drinker', default="Error")
    Units = request.form.get('Units', default="Error")
    Height = request.form.get('Height', default="Error")
    Weight = request.form.get('Weight', default="Error")
    HealthConditions = request.form.get('HealthConditions', default="Error")
    HazardousPursuits = request.form.get('HazardousPursuits', default="Error")

    conn = sqlite3.connect(DATABASE)
    details = [(GoodHealth, Smoker, SmokeADay, Drinker, Units, Height, Weight, HealthConditions, HazardousPursuits)]
    conn.executemany("INSERT INTO `Health`('GoodHealth', 'Smoker', 'SmokeADay',\
                     'Drinker', 'Units', 'Height', 'Weight', 'HealthConditions', 'HazardousPursuits') VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)"
                     , details)
    conn.commit()
    conn.close()
    msg = "Completed."
    return redirect(url_for('health'))   

@app.route("/Client/ClientInsert", methods=['POST'])
def ClientAddDetails():
    AccountID = request.form.get('AccountID', default="Error")
    Forname = request.form.get('Forname', default="Error")
    Surname = request.form.get('Surname', default="Error")
    eMail = request.form.get('eMail', default="Error")
    Username = request.form.get('Username', default="Error")
    Password = request.form.get('Password', default="Error")
    Password = hash_password(Password)

    conn = sqlite3.connect(DATABASE)
    details = [(AccountID, Forname, Surname, eMail, Username, Password)]
    conn.executemany("INSERT INTO `Accounts`('AccountID', 'Forname', 'Surname',\
                     'eMail', 'Username', 'Password') VALUES(?, ?, ?, ?, ?, ?)"
                     , details)
    conn.commit()
    conn.close()
    msg = "Completed."
    return msg


@login_required
@app.route("/AddDetails", methods=['POST'])
def AddDetails():
    firstname = request.form.get('firstname', default="Error")
    surname = request.form.get('surname', default="Error")
    gender = request.form.get('gender', default="Error")
    dob = request.form.get('dob', default="Error")
    address1 = request.form.get('address1', default="Error")
    address2 = request.form.get('address2', default="Error")
    address3 = request.form.get('address3', default="Error")
    address4 = request.form.get('address4', default="Error")
    postcode = request.form.get('postcode', default="Error")
    town = request.form.get('town', default="Error")
    country = request.form.get('country', default="Error")
    phone = request.form.get('phone', default="Error")
    fax = request.form.get('fax', default="Error")
    mobile = request.form.get('mobile', default="Error")
    email = request.form.get('email', default="Error")
    taxstatus = request.form.get('taxstatus', default="Error")
    occupation = request.form.get('occupation', default="Error")
    religion = request.form.get('religion', default="Error")
    circumstances = request.form.get('circumstances', default="Error")

    conn = sqlite3.connect(DATABASE)
    details = [(firstname, surname, gender, dob, address1, address2, address3,
               address4, postcode, town, country, phone, fax, mobile, email,
               taxstatus, occupation, religion, circumstances)]
    conn.executemany("INSERT INTO `Clients`('firstname', 'surname', 'gender',\
                     'dob', 'address1', 'address2', 'address3', 'address4',\
                     'postcode', 'town', 'country', 'phone', 'fax', 'mobile',\
                     'email', 'taxstatus', 'occupation', 'religion',\
                     'circumstances') \
                     VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,\
                            ?, ?)", details)
    conn.commit()
    conn.close()
    msg = "Details Added."
    return msg


@app.route("/Client/ClientAdd")
@login_required
def ClientAdd():
    return render_template('ClientData.html', msg='')

@app.route("/AddClient")
@login_required
def customer():
    return render_template('clientdetail.html', msg='')


@app.route("/Client")
@login_required
def clients():
    return render_template('people/clients.html', msg='')


@app.route("/AddDetails")
@login_required
def details():
    return render_template('clientdetail.html', msg='')


@app.route("/taxStatus")
@login_required
def taxStatus():
    return render_template('people/taxStatus.html', msg='')


@app.route("/Occupation")
@login_required
def occupation():
    return render_template('people/occupation.html', msg='')


@app.route("/Dependants")
@login_required
def dependants():
    return render_template('people/dependants.html', msg='')


@app.route("/Health", methods=['GET'])
@login_required
def health():
    return render_template('people/health.html', msg='')


@app.route("/Expenditure")
@login_required
def expenditure():
    return render_template('finances/expenditure.html', msg='')


@app.route("/Income")
@login_required
def income():
    return render_template('finances/income.html', msg='')


@app.route("/Liabilities")
@login_required
def liabilities():
    return render_template('finances/liabilities.html', msg='')


@app.route("/Affordability")
@login_required
def affordability():
    return render_template('finances/affordability.html', msg='')


@app.route("/Assets")
@login_required
def assets():
    return render_template('finances/assets.html', msg='')

if __name__ == "__main__":
    app.run(debug=True)
