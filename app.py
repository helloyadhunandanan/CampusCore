from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)
app.secret_key = 'nexus_secret_key'

# --- MySQL Configuration ---
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'ynadmin' # Ensure this matches your local password
app.config['MYSQL_DB'] = 'crms'

mysql = MySQL(app)

# --- 1. Main Routes ---

@app.route('/')
def home():
    """Renders the landing page with login modal."""
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    """Protected route for the Student Dashboard."""
    if 'loggedin' in session:
        return render_template('dashboard.html', name=session['name'])
    return redirect(url_for('home'))

# --- 2. Authentication Module ---

@app.route('/register', methods=['POST'])
def register():
    """Handles new student registration."""
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    
    cursor = mysql.connection.cursor()
    try:
        # Check if user already exists
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        account = cursor.fetchone()
        
        if account:
            return jsonify({"message": "Email already exists"}), 400
        
        # Insert new student
        cursor.execute('INSERT INTO users (name, email, password, role) VALUES (%s, %s, %s, "student")', 
                       (name, email, password))
        mysql.connection.commit()
        return jsonify({"message": "Registration successful"}), 201
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    finally:
        cursor.close()

@app.route('/login_user', methods=['POST'])
def login_user():
    """Handles student login and session creation."""
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM users WHERE email = %s AND password = %s', (email, password))
    user = cursor.fetchone()
    cursor.close()
    
    if user:
        # Create session data
        session['loggedin'] = True
        session['user_id'] = user['user_id']
        session['name'] = user['name']
        session['email'] = user['email']
        return jsonify({"user": user['name']}), 200
    else:
        return jsonify({"message": "Invalid email or password"}), 401

@app.route('/logout')
def logout():
    """Clears the session and logs out the user."""
    session.clear()
    return redirect(url_for('home'))

# --- 3. Dashboard Data Module ---

@app.route('/get_user_data')
def get_user_data():
    """Fetches bookings and issues for the logged-in user."""
    if 'loggedin' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    
    user_id = session['user_id']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    # Fetch student's bookings
    cursor.execute('SELECT resource_id, status FROM bookings WHERE user_id = %s', (user_id,))
    bookings = cursor.fetchall()
    
    # Fetch student's reported issues
    cursor.execute('SELECT description, status FROM issues WHERE user_id = %s', (user_id,))
    issues = cursor.fetchall()
    
    cursor.close()
    return jsonify({
        "bookings": bookings,
        "issues": issues
    })

if __name__ == '__main__':
    # host='0.0.0.0' allows access from mobile devices on the same Wi-Fi
    app.run(debug=True, host='0.0.0.0')
