import os
from flask import Flask, redirect, url_for, request, render_template, jsonify
import sqlite3

app = Flask(__name__)

DATABASE = 'database.db'

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


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
        cur.execute("SELECT * FROM Accounts WHERE Username=? AND Password=?",
                    (username, password))
        outcome = cur.fetchall()
        if len(outcome) > 0:
            return "/Client"
        else:
            return "/Login"


@app.route("/Client/ClientInsert", methods=['POST'])
def ClientAddDetails():
    AccountID = request.form.get('AccountID', default="Error")
    Forname = request.form.get('Forname', default="Error")
    Surname = request.form.get('Surname', default="Error")
    eMail = request.form.get('eMail', default="Error")
    Username = request.form.get('Username', default="Error")
    Password = request.form.get('Password', default="Error")

    conn = sqlite3.connect(DATABASE)
    details = [(AccountID, Forname, Surname, eMail, Username, Password)]
    conn.executemany("INSERT INTO `Accounts`('AccountID', 'Forname', 'Surname',\
                     'eMail', 'Username', 'Password') VALUES(?, ?, ?, ?, ?, ?)"
                     , details)
    conn.commit()
    conn.close()
    msg = "Completed."
    return msg


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
def ClientAdd():
    return render_template('ClientData.html', msg='')


@app.route("/AddClient")
def customer():
    return render_template('clientdetail.html', msg='')


@app.route("/Client")
def clients():
    return render_template('people/clients.html', msg='')


@app.route("/AddDetails")
def details():
    return render_template('clientdetail.html', msg='')


@app.route("/taxStatus")
def taxStatus():
    return render_template('people/taxStatus.html', msg='')


@app.route("/Occupation")
def occupation():
    return render_template('people/occupation.html', msg='')


@app.route("/Dependants")
def dependants():
    return render_template('people/dependants.html', msg='')


@app.route("/Health")
def health():
    return render_template('people/health.html', msg='')


@app.route("/Expenditure")
def expenditure():
    return render_template('finances/expenditure.html', msg='')


@app.route("/Income")
def income():
    return render_template('finances/income.html', msg='')


@app.route("/Liabilities")
def liabilities():
    return render_template('finances/liabilities.html', msg='')


@app.route("/Affordability")
def affordability():
    return render_template('finances/affordability.html', msg='')


@app.route("/Assets")
def assets():
    return render_template('finances/assets.html', msg='')

if __name__ == "__main__":
    app.run(debug=True)
