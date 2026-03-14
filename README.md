# 🏛️ NEXUS – Campus Resource Management System (CRMS)

![Python](https://img.shields.io/badge/Python-3-blue)
![Flask](https://img.shields.io/badge/Framework-Flask-green)
![Database](https://img.shields.io/badge/Database-MySQL-orange)
![License](https://img.shields.io/badge/License-MIT-red)

**NEXUS (Campus Resource Management System)** is a smart platform designed to streamline the **booking, scheduling, and maintenance of university resources**.

It provides a **secure role-based environment** where **students, staff, Head of Departments (HODs), and administrators** can efficiently manage and reserve:

* 🧪 Labs
* 🏛️ Venues
* 🎤 Equipment
* 🏫 Centralised Campus Facilities

The system improves **resource utilization, transparency, and operational efficiency across campus infrastructure.**

---

# ✨ Key Features

## 🔐 Role-Based Access Control (RBAC)

The system provides structured access based on user roles.

### 👨‍🎓 Students / Staff

* View resource availability and schedules
* Request resource bookings
* Cancel their own bookings
* Report equipment issues

### 👨‍🏫 HOD (Head of Department)

* Receive department-specific booking requests
* Approve or reject resource bookings
* Manage departmental resources

### 🛡️ Administrator

* Complete system oversight
* Manage users and roles
* Add and update resources
* Handle issue reports
* Approve bookings for **Centralised Facilities**

Examples:

* Auditoriums
* PA Systems
* Shared Campus Infrastructure

---

# 📅 Smart Scheduling & Conflict Detection

NEXUS includes a **smart scheduling algorithm** to prevent resource conflicts.

The system:

* Parses requested time slots (example: **10:00 – 12:00**)
* Cross-checks existing bookings
* Prevents **overlapping reservations**

This guarantees **conflict-free resource allocation.**

---

# 🏢 Intelligent Department Routing

When a booking request is created:

1. The system identifies **which department owns the resource**
2. The request is routed automatically to the **respective HOD**

### Special Case

Resources under:

**Department ID: 99**
**Department Name: Centralised Facilities**

These booking requests are **directly routed to the Administrator**.

---

# ⚡ Live Search & Filtering

The dashboard supports **instant filtering and searching** using **Vanilla JavaScript**.

Users can quickly search through:

* Resource schedules
* User lists
* Booking requests
* Issue reports

All without **reloading the page**, making the system fast and responsive.

---

# 🛠️ Issue Tracking & Maintenance

NEXUS includes a built-in **issue reporting system**.

Users can report:

* Broken equipment
* Lab issues
* Maintenance problems

Administrators can:

* Track issue status
* Monitor pending repairs
* Mark issues as **Resolved**

---

# 💻 Technology Stack

## Backend

* Python 3
* Flask
* Flask-MySQLdb
* Werkzeug (Password Security)

## Frontend

* HTML5
* CSS3
* Vanilla JavaScript
* FontAwesome Icons
* Glassmorphism UI Design

## Database

* MySQL

---

# 🚀 Installation & Setup

## 1️⃣ Prerequisites

Make sure these are installed:

* Python 3.x
* MySQL Server

---

## 2️⃣ Clone the Repository

```bash
git clone https://github.com/yourusername/nexus-crms.git
cd nexus-crms
```

---

## 3️⃣ Install Dependencies

```bash
pip install Flask Flask-MySQLdb Werkzeug
```

---

## 4️⃣ Create Database

Login to MySQL and create the database.

```sql
CREATE DATABASE crms;
```

Create required tables:

* users
* department
* resources
* bookings
* issues

Important requirement:

Create a department with:

```
department_id = 99
department_name = Centralised Facilities
```

This enables **Admin approval routing**.

---

## 5️⃣ Configure Database in `app.py`

Update MySQL credentials if required.

```python
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'your_password_here'
app.config['MYSQL_DB'] = 'crms'
```

---

## 6️⃣ Run the Application

```bash
python app.py
```

Open the browser and visit:

```
http://127.0.0.1:5000/
```

---

# 📂 Project Structure

```
nexus-crms
│
├── app.py
│   Main Flask application
│
├── templates
│   ├── index.html
│   └── dashboard.html
│
├── static
│   ├── style.css
│   └── script.js
│
└── README.md
```

---

# 🔒 Security Features

NEXUS follows secure development practices.

* Passwords are **hashed using Werkzeug**
* Plain-text passwords are **never stored**
* Session-based authentication
* Restricted routes for sensitive actions

Protected routes include:

* `/approve`
* `/reject`
* `/add_resource`

Additional protection:

* HODs **cannot approve requests from other departments**
* Role-based access enforcement

---

# 📸 Screenshots

Add screenshots of your system here.

Example:

```
Login Page
Dashboard
Booking Interface
Admin Panel
```

---

# 🤝 Contributing

Contributions are welcome.

You can:

* Open issues
* Suggest features
* Submit pull requests

---

# 📝 License

This project is licensed under the **MIT License**.

---

