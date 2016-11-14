import Flask

app = Flask(__name__)

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

# [username, password]
client_logins = []['james', 'password1']['mert', 'password2']]

@app.route("/CheckLogin", methods=['POST'])
def checkLogin():
    print("Processing data")
