import os
from flask import Flask, redirect, url_for, request, render_template, jsonify
import sqlite3

app = Flask(__name__)

DATABASE = 'database.db'

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

# [username, password]
valid_logins = [['james', 'password1', 'client'], ['mert', 'password2', 'IFA']]

@app.route("/Login")
def login():
    return render_template('login/login.html', msg = '')


@app.route("/CheckLogin", methods=['POST'])
def checkLogin():
    print("Processing data")
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()
        cur.execute("SELECT * FROM Accounts WHERE Username=? AND Password=?", (username, password))
        outcome = cur.fetchall()
        if len(outcome) > 0:
            return "/Client"
        else:
            return "/Login"


@app.route("/Client/ClientInsert", methods = ['POST'])
def ClientAddDetails():
    AccountID = request.form.get('AccountID', default="Error")  #rem: args for get form for post
    Forname = request.form.get('Forname', default="Error")
    Surname = request.form.get('Surname', default="Error")
    eMail = request.form.get('eMail', default="Error")
    Username = request.form.get('Username', default="Error")
    Password = request.form.get('Password', default="Error")

    conn = sqlite3.connect(DATABASE)
    details = [(AccountID, Forname, Surname, eMail, Username, Password)]
    conn.executemany("INSERT INTO `Accounts`('AccountID', 'Forname', 'Surname', 'eMail', 'Username', 'Password')\
                    VALUES (?,?,?,?,?,?)",details)
    conn.commit()
    conn.close()
    msg = "Completed."
    return msg

@app.route("/Client/ClientAdd")
def ClientAdd():
	return render_template('ClientData.html', msg = '')

@app.route("/AddClient")
def customer():
	return render_template('AddClient.html', msg = '')

@app.route("/Client")
def clients():
    return render_template('people/clients.html', msg = '')

@app.route("/taxStatus")
def taxStatus():
    return render_template('people/taxStatus.html', msg = '')

@app.route("/Occupation")
def occupation():
    return render_template('people/occupation.html', msg = '')

@app.route("/Dependants")
def dependants():
    return render_template('people/dependants.html', msg = '')

@app.route("/Health")
def health():
    return render_template('people/health.html', msg = '')

@app.route("/Expenditure")
def expenditure():
    return render_template('finances/expenditure.html', msg = '')

@app.route("/Income")
def income():
    return render_template('finances/income.html', msg = '')

@app.route("/Liabilities")
def liabilities():
    return render_template('finances/liabilities.html', msg = '')

@app.route("/Affordability")
def affordability():
    return render_template('finances/affordability.html', msg = '')

@app.route("/Assets")
def assets():
    return render_template('finances/assets.html', msg = '')

if __name__ == "__main__":
    app.run(debug=True)
