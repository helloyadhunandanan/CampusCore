NEXUS - Campus Resource Management System (CRMS) 🏛️

NEXUS is a comprehensive, premium Campus Resource Management System designed to streamline the booking and maintenance of university assets. It provides a secure, role-based platform for students, staff, Head of Departments (HODs), and Administrators to seamlessly reserve labs, venues, equipment, and centralized campus facilities.

✨ Key Features

🔐 Advanced Role-Based Access Control (RBAC)

Students/Staff: Can view campus schedules, request resource bookings, cancel their own bookings, and report issues.

HOD (Head of Department): Receives routing for booking requests specific to their department's resources. Can securely approve or reject requests.

Administrator: Has global oversight. Manages user roles, adds new resources, resolves reported issues, and specifically handles approvals for "Centralised Facilities" (e.g., PA Systems, Main Auditoriums).

📅 Smart Scheduling & Conflict Detection

Algorithm automatically parses requested time slots (e.g., "10:00 to 12:00") and cross-references them against approved and pending bookings.

Mathematically prevents overlapping bookings on the same resource on the same date.

🏢 Intelligent Department Routing

When a user requests a resource, the system dynamically identifies which department owns that resource and routes the approval request to that specific HOD.

Includes a specialized routing bypass for Department 99 (Centralised Facilities), sending those requests straight to the global Administrator.

⚡ Live Search & Filtering

Lightning-fast vanilla JavaScript filtering applied across all dashboard tables.

Users can instantly search through schedules, user lists, issues, and pending approvals without reloading the page.

🛠️ Issue Tracking & Maintenance

Integrated ticketing system allowing users to report broken equipment or general campus issues.

Admins can track and mark issues as "Resolved" directly from the dashboard.

💻 Tech Stack

Backend:

Python 3

Flask

Flask-MySQLdb

Werkzeug (for secure password hashing)

Frontend:

HTML5 / CSS3

Vanilla JavaScript

FontAwesome (Icons)

Custom Glassmorphism UI Design

Database:

MySQL

🚀 Installation & Setup

1. Prerequisites

Ensure you have Python 3.x and MySQL Server installed on your machine.

2. Clone the Repository

git clone [https://github.com/yourusername/nexus-crms.git](https://github.com/yourusername/nexus-crms.git)
cd nexus-crms


3. Install Dependencies

It is recommended to use a virtual environment.

pip install Flask Flask-MySQLdb Werkzeug


4. Database Configuration

Log in to your MySQL server.

Create a database named crms:

CREATE DATABASE crms;


Set up the required tables: users, department, resources, bookings, and issues.
(Ensure you create a department with department_id = 99 named "Centralised Facilities" for Admin routing to work properly).

Update the database credentials in app.py if your local MySQL setup uses a different password:

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'your_password_here'
app.config['MYSQL_DB'] = 'crms'


5. Run the Application

python app.py


The application will be live at http://127.0.0.1:5000/.

📸 Application Structure

app.py: The core Flask application handling routing, session management, and database interactions.

templates/: Contains HTML files.

index.html: Login and Registration portal.

dashboard.html: The main, dynamic glassmorphism dashboard that adapts based on user roles.

static/: Contains style.css and script.js for theme toggling and UI enhancements.

🔒 Security Notes

Passwords are never stored in plain text. The system utilizes generate_password_hash and check_password_hash via Werkzeug.

Session-based authentication strictly locks down routes (/approve, /reject, /add_resource) to authorized roles only.

HODs are cryptographically blocked from approving requests for departments they do not oversee.

🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page.

📝 License

This project is licensed under the MIT License.
