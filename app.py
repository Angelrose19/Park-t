from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)
app.secret_key = 'your secret key'

# database config
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'geeklogin'
mysql = MySQL(app)

@app.route('/')
def index():
    if 'loggedin' in session:
        if 'role' in session:
            # Redirect to profile page based on role
            if session['role'] == 'driver':
                return redirect(url_for('profile_driver'))
            elif session['role'] == 'owner':
                return redirect(url_for('profile_owner'))
        else:
            return redirect(url_for('logout'))  # Logout if role not found in session
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password,))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            session['role'] = account['role']  # Store role in session
            return redirect(url_for('index'))
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg=msg)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    session.pop('role', None)  # Remove role from session
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        mobile = request.form['mobile']  
        role = request.form['role']  # Get role from form
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO accounts (username, password, email, mobile, role) VALUES (%s, %s, %s, %s, %s)', (username, password, email, mobile, role,))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg=msg)

# Profile routes based on role
@app.route('/profile_driver')
def profile_driver():
    # Check if the user is logged in
    if 'loggedin' in session:
        conn = mysql.connection
        cursor = conn.cursor(MySQLdb.cursors.DictCursor)

        # Query to fetch parking space data
        cursor.execute('SELECT location, latitude, longitude FROM parking_spaces')
        parking_spaces = cursor.fetchall()

        # Render the driver profile page with parking space data
        return render_template('profile_driver.html', parking_spaces=parking_spaces)
    # Redirect to login if the user is not logged in
    return redirect(url_for('login'))

@app.route('/profile_owner')
def profile_owner():
    if 'loggedin' in session and session['role'] == 'owner':
        # Fetch registered parking spaces from the database
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM parking_spaces WHERE owner_id = %s', (session['id'],))
        parking_spaces = cursor.fetchall()
        return render_template('profile_owner.html', username=session['username'], parking_spaces=parking_spaces)
    return redirect(url_for('login'))

# Route for adding new parking space
@app.route('/add_parking_space', methods=['POST'])
def add_parking_space():
    if 'loggedin' in session and session['role'] == 'owner':
        if request.method == 'POST':
            location = request.form['location']
            total_slots = request.form['total_slots']
            address = request.form['address']
            latitude = request.form['latitude']
            longitude = request.form['longitude']
            owner_id = session['id']
            cursor = mysql.connection.cursor()
            cursor.execute('INSERT INTO parking_spaces (location, total_slots, address, latitude, longitude, owner_id) VALUES (%s, %s, %s, %s, %s, %s)',
                           (location, total_slots, address, latitude, longitude, owner_id,))
            mysql.connection.commit()
            cursor.close()
        return redirect(url_for('profile_owner'))
    return redirect(url_for('login'))

# Route to handle the delete request for a parking space entry
@app.route('/delete_parking_space/<int:id>', methods=['POST'])
def delete_parking_space(id):
    if 'loggedin' in session and session['role'] == 'owner':
        # Delete the parking space entry from the database
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM parking_spaces WHERE id = %s", (id,))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('profile'))
    else:
        return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)
