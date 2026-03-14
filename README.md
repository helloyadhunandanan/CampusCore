🏛️ NEXUS – Campus Resource Management System (CRMS)

NEXUS is a comprehensive and premium Campus Resource Management System designed to streamline the booking, scheduling, and maintenance of university resources.

It provides a secure, role-based platform where students, staff, Head of Departments (HODs), and administrators can efficiently manage and reserve labs, venues, equipment, and centralized campus facilities.

The system improves resource utilization, transparency, and operational efficiency across the campus.

✨ Key Features
🔐 Advanced Role-Based Access Control (RBAC)

The system ensures secure access using structured role permissions.

Students / Staff

View campus resource schedules

Request bookings for labs, venues, and equipment

Cancel their own bookings

Report equipment issues or campus problems

HOD (Head of Department)

Receives booking requests related to their department resources

Can approve or reject booking requests

Manages departmental resource usage efficiently

Administrator

Has complete system oversight

Manages user roles and permissions

Adds and manages campus resources

Handles issue resolution

Approves bookings for Centralised Facilities such as:

Main Auditoriums

PA Systems

Shared Campus Infrastructure

📅 Smart Scheduling & Conflict Detection

The system uses a smart scheduling algorithm to avoid resource conflicts.

Automatically parses requested time slots (example: 10:00 AM – 12:00 PM)

Compares the request with existing approved and pending bookings

Prevents overlapping reservations for the same resource on the same date

This ensures fair and conflict-free scheduling.

🏢 Intelligent Department Routing

The booking workflow is automated through department-based routing.

When a booking request is created, the system identifies which department owns the resource.

The request is automatically routed to the respective HOD for approval.

Special Case

Resources under Department ID 99 – Centralised Facilities are directly routed to the Administrator for approval.

This ensures efficient approval workflows and faster processing.

⚡ Live Search & Filtering

The system provides instant search and filtering capabilities.

Implemented using Vanilla JavaScript

Users can quickly filter:

Resource schedules

User lists

Booking requests

Issue reports

All filtering happens without page reloads, ensuring a fast and responsive dashboard experience.

🛠️ Issue Tracking & Maintenance System

NEXUS includes an integrated issue management module.

Users can:

Report broken equipment

Submit campus maintenance requests

Administrators can:

Track reported issues

Monitor issue status

Mark issues as Resolved

This helps maintain campus infrastructure efficiently.

💻 Technology Stack
Backend

Python 3

Flask

Flask-MySQLdb

Werkzeug (Secure Password Hashing)

Frontend

HTML5

CSS3

Vanilla JavaScript

FontAwesome (Icons)

Custom Glassmorphism UI Design

Database

MySQL

🚀 Installation & Setup
1️⃣ Prerequisites

Make sure the following are installed on your system:

Python 3.x

MySQL Server

2️⃣ Clone the Repository
git clone https://github.com/yourusername/nexus-crms.git
cd nexus-crms

3️⃣ Install Dependencies

It is recommended to use a Python virtual environment.

pip install Flask Flask-MySQLdb Werkzeug

4️⃣ Database Configuration

Login to MySQL and create a database:

CREATE DATABASE crms;


Create the required tables:

users

department

resources

bookings

issues

⚠️ Important Requirement

Create a department with:

department_id = 99
department_name = "Centralised Facilities"


This is required for Administrator approval routing.

Configure Database in app.py

Update the MySQL credentials if required:

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'your_password_here'
app.config['MYSQL_DB'] = 'crms'

5️⃣ Run the Application
python app.py


Open your browser and visit:

http://127.0.0.1:5000/

📂 Application Structure
nexus-crms/
│
├── app.py
│   Core Flask application handling routing,
│   authentication, and database interactions
│
├── templates/
│   ├── index.html
│   │   Login and Registration Portal
│   │
│   └── dashboard.html
│       Role-based dynamic glassmorphism dashboard
│
├── static/
│   ├── style.css
│   └── script.js
│       UI styling, search filtering, and theme controls

🔒 Security Features

NEXUS follows secure coding practices:

Passwords are never stored in plain text

Uses Werkzeug password hashing

generate_password_hash

check_password_hash

Session-based authentication

Route protection for sensitive actions:

/approve

/reject

/add_resource

Additional Security:

HODs cannot approve requests outside their department

Access is restricted based on user roles

🤝 Contributing

Contributions, improvements, and feature requests are welcome.

You can:

Open issues

Submit pull requests

Suggest new features

📝 License

This project is licensed under the MIT License.
