import os
from flask import Flask, redirect, request, render_template, jsonify

app = Flask(__name__)

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

# [username, password]
valid_logins = [['james', 'password1'], ['mert', 'password2']]

@app.route("/CheckLogin", methods=['POST'])
def checkLogin():
    print("Processing data")
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        the_login = [username, password]

        if the_login in valid_logins:
            return 'login successful'
        else:
            return 'login failed'
