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
# This function is a Python decorator which checks the user is logged in
# Using the session object. If signed in the user gets taken to the page
# Else the user is taken to the login page
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
# Same as login_required but checks for admin in the session
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            if session['admin'] is None:
                return redirect(url_for('login', next=request.url))
            return f(*args, **kwargs)
        except KeyError:
            return redirect(url_for('login', next=request.url))
    return decorated_function


# Adapted from http://pythoncentral.io/hashing-strings-with-python/
# Generates random salt, encrypts this and the entered password using sha256
# then attaches the unencrypted salt after a colon
def hash_password(password):
    # uuid is used to generate a random number
    salt = uuid.uuid4().hex
    return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':'\
        + salt


# Adapted from http://pythoncentral.io/hashing-strings-with-python/
# Splits the encrypted block from the salt. Then runs the password and salt
# encryption from hash_password and checks to see if the results match
def hashed_password(hashed_password, user_password):
    password, salt = hashed_password.split(':')
    return hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()\
        + ":" + salt


# This AppRoute takes the user to the login page
@app.route("/Login")
def login():
    return render_template('login/login.html', msg='')


# This AppRoute is used to check the client login as well as add the user to the
# Session object if login is successful
@app.route("/CheckClientLogin", methods=['POST'])
def checkClientLogin():
    print("Processing data")
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Find the users password salt.
        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()
        cur.execute("SELECT Password FROM ClientAccounts WHERE Username=?",
                    (username,))
        actual_password = cur.fetchall()
        actual_password = actual_password[0][0]

        # As long as the account exists
        if actual_password != "":
            password = hashed_password(actual_password, password)
            cur.execute("SELECT * FROM ClientAccounts WHERE Username=? AND\
            Password=?", (username, password))
            outcome = cur.fetchall()

            # If password matched the database
            if len(outcome) > 0:
                session['user'] = username
                return "/Client"
            else:
                return "/Login"

# This AppRoute checks login as ClientLogin does but from IFAAccounts table
@app.route("/CheckIFALogin", methods=['POST'])
def checkIFALogin():
    print("Processing data")
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()
        cur.execute("SELECT Password FROM IFAAccounts WHERE Username=?",
                    (username,))
        actual_password = cur.fetchall()
        actual_password = actual_password[0][0]
        if actual_password != "":
            password = hashed_password(actual_password, password)
            cur.execute("SELECT * FROM IFAAccounts WHERE Username=? AND\
            Password=?", (username, password))
            outcome = cur.fetchall()
            if len(outcome) > 0:
                session['user'] = username
                return "/Client"
            else:
                return "/Login"

# This AppRoute removes the user from the session and redirects to the login page
@app.route("/Logout")
def logout():
    session['user'] = None
    session['admin'] = None
    return redirect(url_for('login'))

# This AppRoute takes the user input from the form on the health page and uploads the data to the database
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
    details = [(GoodHealth, Smoker, SmokeADay, Drinker, Units, Height, Weight,
                HealthConditions, HazardousPursuits)]
    conn.executemany("INSERT INTO `Health`('GoodHealth', 'Smoker', 'SmokeADay',\
                     'Drinker', 'Units', 'Height', 'Weight',\
                     'HealthConditions', 'HazardousPursuits') VALUES(?, ?, ?,\
                     ?, ?, ?, ?, ?, ?)", details)
    conn.commit()
    conn.close()
    msg = "Completed."
    return redirect(url_for('health'))

# This AppRoute takes the user input from the form on the dependants page and uploads the data to the database
@app.route("/DependantsData", methods=['POST'])
def DependantsData():
    Type = request.form.get('Type', default="Error")
    Title = request.form.get('Title', default="Error")
    FirstName = request.form.get('FirstName', default="Error")
    Initials = request.form.get('Initials', default="Error")
    LastName = request.form.get('LastName', default="Error")
    KnownAs = request.form.get('KnownAs', default="Error")
    Sex = request.form.get('Sex', default="Error")
    DOB = request.form.get('DOB', default="Error")
    Age = request.form.get('Age', default="Error")
    Relationship = request.form.get('Relationship', default="Error")
    FinanciallyDependent = request.form.get('FinanciallyDependent',
                                            default="Error")
    Notes = request.form.get('Notes', default="Error")
    conn = sqlite3.connect(DATABASE)
    details = [(Type, Title, FirstName, Initials, LastName, KnownAs, Sex, DOB,
                Age, Relationship, FinanciallyDependent, Notes)]
    conn.executemany("INSERT INTO `Dependants`('Type', 'Title', 'FirstName',\
                     'Initials', 'LastName', 'KnownAs', 'Sex', 'DOB',\
                     'Age', 'Relationship', 'FinanciallyDependent', 'Notes')\
                     VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                     details)
    conn.commit()
    conn.close()
    msg = "Completed."
    return redirect(url_for('dependants'))

#The below app route creates the account for a client
@app.route("/Client/ClientInsert", methods=['POST'])
def ClientAddDetails():
    Forname = request.form.get('Forname', default="Error")
    Surname = request.form.get('Surname', default="Error")
    eMail = request.form.get('eMail', default="Error")
    Username = request.form.get('Username', default="Error")
    Password = request.form.get('Password', default="Error")
    Password = hash_password(Password)
    conn = sqlite3.connect(DATABASE)
    details = [(Forname, Surname, eMail, Username, Password)]
    conn.executemany("INSERT INTO `ClientAccounts`('Forname', 'Surname',\
                     'eMail', 'Username', 'Password') VALUES(?, ?, ?, ?, ?)",
                     details)
    conn.commit()
    conn.close()
    msg = "Completed."
    return msg

# Adds a new IFA account to the database
@app.route("/Client/IFAInsert", methods=['POST'])
def IFAAddDetails():
    Forname = request.form.get('Forname', default="Error")
    Surname = request.form.get('Surname', default="Error")
    eMail = request.form.get('eMail', default="Error")
    Username = request.form.get('Username', default="Error")
    Password = request.form.get('Password', default="Error")
    Password = hash_password(Password)
    conn = sqlite3.connect(DATABASE)
    details = [(Forname, Surname, eMail, Username, Password)]
    conn.executemany("INSERT INTO `IFAAccounts`('Forname', 'Surname',\
                     'eMail', 'Username', 'Password') VALUES(?, ?, ?, ?, ?)",
                     details)
    conn.commit()
    conn.close()
    msg = "Completed."
    return msg

# Add personal details for a client to the database.
@login_required
@app.route("/AddDetails", methods=['POST'])
def AddDetails():
    title = request.form.get('title', default="Error")
    firstname = request.form.get('firstname', default="Error")
    initials = request.form.get('initials', default="Error")
    surname = request.form.get('surname', default="Error")
    prefers = request.form.get('prefers', default="Error")
    age = request.form.get('age', default="Error")
    gender = request.form.get('gender', default="Error")
    dob = request.form.get('dob', default="Error")
    maritalstatus = request.form.get('maritalstatus', default="Error")
    maidenname = request.form.get('maidenname', default="Error")
    retire = request.form.get('retire', default="Error")
    taxstatus = request.form.get('taxstatus', default="Error")
    occupation = request.form.get('occupation', default="Error")
    religion = request.form.get('religion', default="Error")
    circumstances = request.form.get('circumstances', default="Error")
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
    conn = sqlite3.connect(DATABASE)
    details = [(title, firstname, initials, surname, prefers, age, gender, dob,
               maritalstatus, maidenname, retire, taxstatus, occupation,
               religion, circumstances, address1, address2, address3, address4,
               postcode, town, country, phone, fax, mobile, email)]
    conn.executemany("INSERT INTO `ClientDetails`('title', 'firstname',\
                     'initials', 'surname', 'prefers', 'age', 'gender', 'dob',\
                     'maritalstatus', 'maidenname', 'retire', 'taxstatus',\
                     'occupation', 'religion', 'circumstances', 'address1',\
                     'address2', 'address3', 'address4', 'postcode', 'town',\
                     'country', 'phone', 'fax', 'mobile', 'email') \
                     VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,\
                            ?, ?, ?, ?, ?, ?, ?, ?, ?)", details)
    conn.commit()
    conn.close()
    msg = "Details Added."
    return msg

# This AppRoute deletes a client from the database
@app.route("/DeleteClient", methods=['GET', 'POST'])
def delCustomer():
    if request.method == 'GET':
        return render_template('deleteClient.html')
    if request.method == 'POST':
        ID_del = str(request.form["ID"])
        conn = sqlite3.connect(DATABASE)
        conn.execute("DELETE FROM `ClientAccounts`\
                        WHERE ClientAccountID = ?", (ID_del,))
        conn.commit()
        conn.close()
        return render_template('deleteClient.html', msg="User Deleted")

# This AppRoute takes the user to the update client page
@app.route("/UpdateClient")
@login_required
def update():
    return render_template('update.html', msg='')

# This AppRoute takes the user to the view client page
@app.route("/ViewClient")
@login_required
def list():
    client_list = getData()
    headings = ["ID", "Forname", "Surname", "E-Mail", "Username", "Password"]
    return render_template('clientlist.html', msg=client_list)

#This retrieves all data in the ClientAccounts table which is used to present a list of clients
def getData():
    msg = []
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('SELECT * FROM ClientAccounts')
    msg.append(c.fetchall())
    msg = msg[0]
    return msg

# This AppRoute takes the user to the Client Data page
@app.route("/Client/ClientAdd")
@login_required
def customer():
    return render_template('ClientData.html', msg='')

# This AppRoute takes the user to the Create IFA page
@app.route("/Client/IFAAdd")
@login_required
def createIFA():
    return render_template('CreateIFA.html', msg='')

# This AppRoute takes the user to the Clients page
@app.route("/Client")
@login_required
def clients():
    return render_template('clients.html', msg='')

# This AppRoute takes the user to the Clietns add page
@app.route("/Client/ClientAdd")
def newaccount():
    return render_template('ClientData.html', msg='')

# This AppRoute takes the user to the Client Detials page
@app.route("/AddDetails")
@login_required
def details():
    return render_template('clientdetail.html', msg='')

# This AppRoute takes the user to the Tax Status page
@app.route("/taxStatus")
@login_required
def taxStatus():
    return render_template('people/taxStatus.html', msg='')

# This AppRoute takes the user to the Occupation page
@app.route("/Occupation")
@login_required
def occupation():
    return render_template('people/occupation.html', msg='')

# This AppRoute takes the user to the Dependants page
@app.route("/Dependants")
@login_required
def dependants():
    return render_template('people/dependants.html', msg='')

# This AppRoute takes the user to the Health page
@app.route("/Health", methods=['GET'])
@login_required
def health():
    return render_template('people/health.html', msg='')

# This AppRoute takes the user to the Expenditure page
@app.route("/Expenditure")
@login_required
def expenditure():
    return render_template('finances/expenditure.html', msg='')

#This Route takes the input from the form and inserts it into the appropriate table in the database
@app.route("/ExpenditureData", methods=['POST'])
def ExpenditureData():
    Property = request.form.get('Property', default="Error")
    Housekeeping = request.form.get('Housekeeping', default="Error")
    Transport = request.form.get('Transport', default="Error")
    Dependents = request.form.get('Dependents', default="Error")
    Pets = request.form.get('Pets', default="Error")
    ProffessionalFees = request.form.get('ProffesionalFees', default="Error")
    CostOfBorrowing = request.form.get('CostOfBorrowing', default="Error")
    RegularSavings = request.form.get('RegularSavings', default="Error")
    ProtectionPolicies = request.form.get('ProtectionPolicies', default="Error")
    Other = request.form.get('Other', default="Error")

    conn = sqlite3.connect(DATABASE)
    details = [(Property, Housekeeping, Transport, Dependents, Pets, ProffessionalFees, CostOfBorrowing, RegularSavings, ProtectionPolicies, Other)]
    conn.executemany("INSERT INTO `Expenditure`('Property', 'HouseKeeping', 'Transport', 'Dependents', 'Pets',\
                     'ProffessionalFees', 'CostOfBorrowing', 'RegularSavings', 'ProtectionPolicies', 'Other') VALUES(?, ?, ?, ?, ?, ?, ? ,? ,? ,?)",
                     details)
    conn.commit()
    conn.close()
    msg = "Completed."
    return redirect(url_for('expenditure'))

# This AppRoute takes the user to the Income page
@app.route("/Income")
@login_required
def income():
    return render_template('finances/income.html', msg='')

# This AppRoute takes the user input from the form on the income page and uploads the data to the database
@app.route("/IncomeData", methods=['POST'])
def IncomeData():
    Employment = request.form.get('Employment', default="Error")
    SelfEmployment = request.form.get('SelfEmployment', default="Error")
    Pensions = request.form.get('Pensions', default="Error")
    InterestOnSavings = request.form.get('InterestOnSavings', default="Error")
    InvestmentIncome = request.form.get('InvestmentIncome', default="Error")
    RentalIncome = request.form.get('RentalIncome', default="Error")
    CapitalDisposals = request.form.get('CapitalDisposals', default="Error")
    Maintenance = request.form.get('Maintenance', default="Error")
    Insurance = request.form.get('Insurance', default="Error")
    StateBenefit = request.form.get('StateBenefit', default="Error")
    Other = request.form.get('Other', default="Error")

    conn = sqlite3.connect(DATABASE)
    details = [(Employment, SelfEmployment, Pensions, InterestOnSavings, InvestmentIncome, RentalIncome, CapitalDisposals, Maintenance, Insurance, StateBenefit, Other)]
    conn.executemany("INSERT INTO `Income`('Employment', 'SelfEmployment', 'Pensions',\
                     'InterestOnSavings', 'InvestmentIncome', 'RentalIncome',\
					 'CapitalDisposals', 'Maintenance', 'Insurance', 'StateBenefit',\
					 'Other') VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                     details)
    conn.commit()
    conn.close()
    msg = "Completed."
    return redirect(url_for('income'))

# This AppRoute takes the user to the Liabilities page
@app.route("/Liabilities")
@login_required
def liabilities():
    return render_template('finances/liabilities.html', msg='')

# This AppRoute takes the user to the affordability page
@app.route("/Affordability")
@login_required
def affordability():
    return render_template('finances/affordability.html', msg='')

# This AppRoute takes the user input from the form on the Affordability page and uploads the data to the database
@app.route("/AffordabilityData", methods=['POST'])
def AffordabilityData():
    TaxActual = request.form.get('TaxActual', default="Error")
    TaxCalculated = request.form.get('TaxCalculated', default="Error")
    CommittedSpending = request.form.get('CommittedSpending', default="Error")
    DiscretionarySpending = request.form.get('DiscretionarySpending', default="Error")
    SpendingSurplus = request.form.get('SpendingSurplus', default="Error")

    conn = sqlite3.connect(DATABASE)
    details = [(TaxActual, TaxCalculated, CommittedSpending, DiscretionarySpending, SpendingSurplus)]
    conn.executemany("INSERT INTO `Affordability`('TaxActual', 'TaxCalculated',\
                     'CommittedSpending', 'DiscretionarySpending', 'SpendingSurplus') VALUES(?, ?, ?, ?, ?)",
                     details)
    conn.commit()
    conn.close()
    msg = "Completed."
    return redirect(url_for('affordability'))

# This AppRoute takes the user to the assets page
@app.route("/Assets")
@login_required
def assets():
    return render_template('finances/assets.html', msg='')

@app.route("/AssetsData", methods=['POST'])
def AssetsData():
    savings = request.form.get('savings', default="0")
    investments = request.form.get('investments', default="0")
    property_total = request.form.get('property', default="0")
    vehicles = request.form.get('vehicles', default="0")
    personal = request.form.get('personal', default="0")
    business= request.form.get('business', default="0")

    conn = sqlite3.connect(DATABASE)
    details = [(savings, investments, property_total, vehicles, personal, business)]
    conn.executemany("INSERT INTO `Assets`('savings', 'investments',\
                     'property', 'vehicles', 'personal', 'business') \
                      VALUES(?, ?, ?, ?, ?, ?)", details)
    conn.commit()
    conn.close()
    msg = "Completed."
    return render_template('finances/assets.html', msg='')

if __name__ == "__main__":
    app.run(debug=True)
