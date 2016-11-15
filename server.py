import os
from flask import Flask, redirect, request, render_template, jsonify

app = Flask(__name__)

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


if __name__ == "__main__":
    app.run(debug=True)
