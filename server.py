import os
from flask import Flask, redirect, request, render_template, jsonify

app = Flask(__name__)

DATABASE = 'database.db'

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

# [username, password]
valid_logins = [['james', 'password1', 'client'], ['mert', 'password2', 'IFA']]

@app.route("/CheckLogin", methods=['POST'])
def checkLogin():
    print("Processing data")
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        the_login_client = [username, password, "client"]
        the_login_IFA = [username, password, "IFA"]

        if the_login_client in valid_logins:
            return 'login successful. User is client'
        elif the_login_IFA in valid_logins:
            return 'login successful. User is IFA'
        else:
            return 'Login failed'


@app.route("/Client/ClientInsert", methods = ['POST'])
def ClientAddDetails():
    AccountID = request.form.get('AccountID', default="Error")#rem: args for get form for post
    Forname = request.form.get('Forname', default="Error")
    Surname = request.form.get('Surname', default="Error")
    eMail = request.form.get('eMail', default="Error")
    Username = request.form.get('Username', default="Error")
    Password = request.form.get('Password', default="Error")
    try:
        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()
        cur.execute("INSERT INTO Accounts ('AccountID', 'Forname', 'Surname', 'eMail', 'Username', 'Password')\
                     VALUES (?,?,?,?)",(AccountID, Forname, Surname, eMail, Username, Password) )
        conn.commit()
        msg = "Record successfully added"
    except:
        conn.rollback()
        msg = "error in insert operation"
    finally:
        return msg
        conn.close()

@app.route("/Client/ClientAdd")
def ClientAdd():
	return render_template('ClientData.html', msg = '')

@app.route("/AddClient")
def customer():
	return render_template('AddClient.html', msg = '')


if __name__ == "__main__":
    app.run(debug=True)
