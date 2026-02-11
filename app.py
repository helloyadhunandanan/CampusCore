from flask import Flask, request, jsonify, render_template, session
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)
app.secret_key = 'nexus_secret_key'

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'ynadmin'
app.config['MYSQL_DB'] = 'crms'

mysql = MySQL(app)

@app.route('/')
def home():
    # Flask looks inside the /templates/ folder for this file
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    role = 'student' 

    cur = mysql.connection.cursor()
    try:
        cur.execute("INSERT INTO users (name, email, password, role) VALUES (%s, %s, %s, %s)", 
                    (name, email, password, role))
        mysql.connection.commit()
        return jsonify({"message": "Registration successful!"}), 201
    except Exception as e:
        return jsonify({"message": str(e)}), 400
    finally:
        cur.close()

@app.route('/login_user', methods=['POST'])
def login_user():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
    user = cur.fetchone()
    cur.close()

    if user:
        session['loggedin'] = True
        session['user_id'] = user['user_id'] 
        session['name'] = user['name']
        return jsonify({
            "message": "Login successful", 
            "user": user['name']
        }), 200
    else:
        return jsonify({"message": "Invalid email or password"}), 401

if __name__ == '__main__':
    app.run(debug=True)