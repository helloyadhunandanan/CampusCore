from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'crms_premium_secret_key'

# Database Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'ynadmin'
app.config['MYSQL_DB'] = 'crms'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route('/')
def index():
    if 'user_id' in session: 
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE email = %s", [email])
    user = cur.fetchone()
    cur.close()
    
    if user and check_password_hash(user['password'], password):
        session['user_id'] = user['user_id']
        session['name'] = user['name']
        session['role'] = user['role']
        session['department_id'] = user['department_id']
        return redirect(url_for('dashboard'))
    
    flash('Login Failed: Invalid email or password.', 'error')
    return redirect(url_for('index'))

@app.route('/register', methods=['POST'])
def register():
    name = request.form['name']
    dept_name = request.form['department']
    email = request.form['email']
    password = generate_password_hash(request.form['password'])
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT department_id FROM department WHERE department_name = %s", [dept_name])
    dept_result = cur.fetchone()
    
    if not dept_result:
        flash(f"Error: Department '{dept_name}' does not exist.", "error")
        cur.close()
        return redirect(url_for('index'))
        
    try:
        cur.execute("INSERT INTO users (name, email, password, role, department_id) VALUES (%s, %s, %s, 'student', %s)", 
                    (name, email, password, dept_result['department_id']))
        mysql.connection.commit()
        flash("Account created successfully. Please log in.", "success")
    except Exception as e:
        flash("Email already registered or invalid data.", "error")
        
    cur.close()
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.clear()
    flash("Successfully logged out.", "success")
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session: return redirect(url_for('index'))
    cur = mysql.connection.cursor()
    
    # --- ADMIN DATA ---
    all_users = []
    all_issues = []
    all_depts = []
    if session['role'] == 'admin':
        cur.execute("SELECT u.user_id, u.name, u.email, u.role, d.department_name FROM users u LEFT JOIN department d ON u.department_id = d.department_id ORDER BY u.role, u.name")
        all_users = cur.fetchall()
        
        cur.execute("""
            SELECT i.issue_id, COALESCE(r.resource_name, 'General/Other Issue') AS resource_name, 
                   u.name as reported_by, i.description, i.status 
            FROM issues i 
            LEFT JOIN resources r ON i.resource_id = r.resource_id 
            JOIN users u ON i.reported_by = u.user_id 
            ORDER BY i.status DESC
        """)
        all_issues = cur.fetchall()
        cur.execute("SELECT * FROM department")
        all_depts = cur.fetchall()
        
    # --- COMMON DATA ---
    cur.execute("SELECT * FROM resources WHERE status = 'available'")
    resources = cur.fetchall()
    
    cur.execute("SELECT b.booking_id, r.resource_name, b.booking_date, b.time_slot, b.status, b.purpose FROM bookings b JOIN resources r ON b.resource_id = r.resource_id WHERE b.user_id = %s ORDER BY b.booking_date DESC", [session['user_id']])
    my_bookings = cur.fetchall()
    
    cur.execute("""
        SELECT r.resource_name, b.booking_date, b.time_slot, b.status 
        FROM bookings b 
        JOIN resources r ON b.resource_id = r.resource_id 
        WHERE b.status IN ('approved', 'pending') AND b.booking_date >= CURDATE()
        ORDER BY b.booking_date ASC, b.time_slot ASC
    """)
    campus_schedule = cur.fetchall()

    cur.execute("""
        SELECT i.issue_id, COALESCE(r.resource_name, 'General/Other Issue') AS resource_name, 
               i.description, i.status 
        FROM issues i 
        LEFT JOIN resources r ON i.resource_id = r.resource_id 
        WHERE i.reported_by = %s
    """, [session['user_id']])
    my_issues = cur.fetchall()
        
    # --- PENDING APPROVALS LOGIC (HOD & ADMIN) ---
    approvals = []
    if session['role'] == 'hod':
        # FIXED: Added JOIN on department to get requester's department name
        cur.execute("""
            SELECT b.booking_id, u.name, req_dept.department_name AS requester_dept, r.resource_name, b.booking_date, b.time_slot, b.purpose 
            FROM bookings b 
            JOIN users u ON b.user_id = u.user_id 
            LEFT JOIN department req_dept ON u.department_id = req_dept.department_id
            JOIN resources r ON b.resource_id = r.resource_id 
            WHERE b.department_id = %s AND b.status = 'pending'
        """, [session['department_id']])
        approvals = cur.fetchall()
    elif session['role'] == 'admin':
        # FIXED: Added JOIN on department to get requester's department name
        cur.execute("""
            SELECT b.booking_id, u.name, req_dept.department_name AS requester_dept, r.resource_name, b.booking_date, b.time_slot, b.purpose 
            FROM bookings b 
            JOIN users u ON b.user_id = u.user_id 
            LEFT JOIN department req_dept ON u.department_id = req_dept.department_id
            JOIN resources r ON b.resource_id = r.resource_id 
            WHERE b.department_id = 99 AND b.status = 'pending'
        """)
        approvals = cur.fetchall()
        
    cur.close()

    if session['role'] == 'admin':
        return render_template('dashboard.html', users=all_users, issues=all_issues, departments=all_depts, resources=resources, bookings=my_bookings, my_issues=my_issues, approvals=approvals, campus_schedule=campus_schedule)
    else:
        return render_template('dashboard.html', resources=resources, bookings=my_bookings, my_issues=my_issues, approvals=approvals, campus_schedule=campus_schedule)

@app.route('/book', methods=['POST'])
def book():
    if 'user_id' not in session or 'department_id' not in session: 
        session.clear()
        flash("Your session is invalid. Please log in again.", "error")
        return redirect(url_for('index'))
        
    cur = mysql.connection.cursor()
    
    start_time_str = request.form['start_time']
    end_time_str = request.form['end_time']
    time_slot = f"{start_time_str} to {end_time_str}"
    purpose = request.form['purpose']
    resource_id = request.form['resource_id']
    booking_date = request.form['date']
    
    try:
        req_start = datetime.strptime(start_time_str, '%H:%M').time()
        req_end = datetime.strptime(end_time_str, '%H:%M').time()
        if req_start >= req_end:
            flash("Invalid time: End time must be after the start time.", "error")
            return redirect(url_for('dashboard'))
    except ValueError:
        flash("Invalid time format.", "error")
        return redirect(url_for('dashboard'))

    cur.execute("SELECT department_id FROM resources WHERE resource_id = %s", [resource_id])
    res_data = cur.fetchone()
    
    if not res_data:
        flash("Invalid resource selected.", "error")
        return redirect(url_for('dashboard'))
        
    resource_dept_id = res_data['department_id']
    
    cur.execute("SELECT time_slot FROM bookings WHERE resource_id=%s AND booking_date=%s AND status!='rejected'", 
                (resource_id, booking_date))
    existing_bookings = cur.fetchall()
    
    conflict = False
    for b in existing_bookings:
        try:
            b_start_str, b_end_str = b['time_slot'].split(' to ')
            b_start = datetime.strptime(b_start_str.strip(), '%H:%M').time()
            b_end = datetime.strptime(b_end_str.strip(), '%H:%M').time()
            if req_start < b_end and req_end > b_start:
                conflict = True
                break
        except ValueError:
            continue
            
    if conflict:
        flash("Resource is already booked during this overlapping time frame.", "error")
    else:
        cur.execute("INSERT INTO bookings (booking_date, time_slot, user_id, resource_id, department_id, purpose) VALUES (%s, %s, %s, %s, %s, %s)",
                    (booking_date, time_slot, session['user_id'], resource_id, resource_dept_id, purpose))
        mysql.connection.commit()
        flash("Booking request submitted successfully.", "success")
        
    cur.close()
    return redirect(url_for('dashboard'))

@app.route('/approve/<int:booking_id>')
def approve(booking_id):
    if session.get('role') not in ['hod', 'admin']: return redirect(url_for('dashboard'))
    cur = mysql.connection.cursor()
    
    cur.execute("SELECT department_id FROM bookings WHERE booking_id = %s", [booking_id])
    booking_data = cur.fetchone()
    
    if not booking_data:
        flash("Booking not found.", "error")
        return redirect(url_for('dashboard'))

    is_authorized = False
    if session['role'] == 'hod' and booking_data['department_id'] == session['department_id']:
        is_authorized = True
    elif session['role'] == 'admin' and booking_data['department_id'] == 99:
        is_authorized = True

    if not is_authorized:
        flash("Unauthorized: You cannot approve this booking.", "error")
        cur.close()
        return redirect(url_for('dashboard'))
        
    cur.execute("UPDATE bookings SET status='approved', approved_by=%s WHERE booking_id=%s", (session['user_id'], booking_id))
    mysql.connection.commit()
    cur.close()
    flash("Booking Approved.", "success")
    return redirect(url_for('dashboard'))

@app.route('/reject/<int:booking_id>')
def reject(booking_id):
    if session.get('role') not in ['hod', 'admin']: return redirect(url_for('dashboard'))
    cur = mysql.connection.cursor()
    
    cur.execute("SELECT department_id FROM bookings WHERE booking_id = %s", [booking_id])
    booking_data = cur.fetchone()
    
    if not booking_data:
        flash("Booking not found.", "error")
        return redirect(url_for('dashboard'))

    is_authorized = False
    if session['role'] == 'hod' and booking_data['department_id'] == session['department_id']:
        is_authorized = True
    elif session['role'] == 'admin' and booking_data['department_id'] == 99:
        is_authorized = True

    if not is_authorized:
        flash("Unauthorized: You cannot reject this booking.", "error")
        cur.close()
        return redirect(url_for('dashboard'))
        
    cur.execute("UPDATE bookings SET status='rejected', approved_by=%s WHERE booking_id=%s", (session['user_id'], booking_id))
    mysql.connection.commit()
    cur.close()
    flash("Booking Rejected.", "success")
    return redirect(url_for('dashboard'))

@app.route('/cancel_booking/<int:booking_id>')
def cancel_booking(booking_id):
    if 'user_id' not in session:
        return redirect(url_for('index'))
        
    cur = mysql.connection.cursor()
    
    cur.execute("SELECT * FROM bookings WHERE booking_id = %s AND user_id = %s", (booking_id, session['user_id']))
    booking = cur.fetchone()
    
    if not booking:
        flash("Unauthorized: You can only cancel your own bookings.", "error")
        cur.close()
        return redirect(url_for('dashboard'))
        
    cur.execute("DELETE FROM bookings WHERE booking_id = %s", [booking_id])
    mysql.connection.commit()
    cur.close()
    
    flash("Booking cancelled successfully.", "success")
    return redirect(url_for('dashboard'))

@app.route('/report_issue', methods=['POST'])
def report_issue():
    if 'user_id' not in session or 'department_id' not in session: 
        session.clear()
        flash("Your session is invalid. Please log in again.", "error")
        return redirect(url_for('index'))
        
    res_id = request.form['resource_id']
    final_res_id = None if res_id == '0' else res_id
    
    cur = mysql.connection.cursor()
    
    owner_dept_id = session['department_id']
    if final_res_id:
        cur.execute("SELECT department_id FROM resources WHERE resource_id = %s", [final_res_id])
        res_data = cur.fetchone()
        if res_data:
            owner_dept_id = res_data['department_id']
            
    cur.execute("INSERT INTO issues (resource_id, reported_by, department_id, description, status) VALUES (%s, %s, %s, %s, 'open')",
                (final_res_id, session['user_id'], owner_dept_id, request.form['description']))
    mysql.connection.commit()
    cur.close()
    flash("Issue reported successfully.", "success")
    return redirect(url_for('dashboard'))

@app.route('/resolve_issue/<int:issue_id>')
def resolve_issue(issue_id):
    if session.get('role') != 'admin': return redirect(url_for('dashboard'))
    cur = mysql.connection.cursor()
    cur.execute("UPDATE issues SET status='resolved' WHERE issue_id=%s", (issue_id,))
    mysql.connection.commit()
    cur.close()
    flash("Issue marked as resolved.", "success")
    return redirect(url_for('dashboard'))

@app.route('/add_resource', methods=['POST'])
def add_resource():
    if session.get('role') != 'admin': return redirect(url_for('dashboard'))
    
    resource_type = request.form.get('resource_type')
    
    if resource_type == 'Centralised Facility':
        dept_id = 99
    else:
        dept_id = request.form.get('department_id')
        if not dept_id:
            flash("Error: Please select a department.", "error")
            return redirect(url_for('dashboard'))

    cur = mysql.connection.cursor()
    try:
        cur.execute("INSERT INTO resources (resource_name, resource_type, status, department_id) VALUES (%s, %s, 'available', %s)", 
                    (request.form['resource_name'], resource_type, dept_id))
        mysql.connection.commit()
        flash(f"Resource '{request.form['resource_name']}' added successfully.", "success")
    except Exception as e:
        flash("Database Error: Could not add resource. Check your ENUM settings.", "error")
        print("DB Insert Error:", e) 
    finally:
        cur.close()
        
    return redirect(url_for('dashboard'))

@app.route('/admin/change_role/<int:target_user_id>', methods=['POST'])
def change_role(target_user_id):
    if session.get('role') != 'admin': return redirect(url_for('dashboard'))
    if target_user_id == session['user_id']:
        flash("You cannot change your own Admin role.", "error")
        return redirect(url_for('dashboard'))
    cur = mysql.connection.cursor()
    cur.execute("UPDATE users SET role = %s WHERE user_id = %s", (request.form.get('new_role'), target_user_id))
    mysql.connection.commit()
    cur.close()
    flash("User role updated successfully.", "success")
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
