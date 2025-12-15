Student Management API
A comprehensive RESTful API for managing student records built with Flask and MySQL. This system provides full CRUD operations, JWT authentication, and support for multiple data formats (JSON/XML).

Features
✅ Full CRUD Operations - Create, Read, Update, Delete student records

✅ JWT Authentication - Secure endpoints with token-based auth

✅ Dual Format Support - JSON & XML response formats

✅ Advanced Filtering - Search by name, major, year, GPA

✅ Statistics Dashboard - Comprehensive data analytics

✅ Auto-initialization - Pre-populated with 20 sample students

✅ Input Validation - Comprehensive data validation

✅ Error Handling - Graceful error responses

Tech Stack
Backend: Flask 2.0+

Database: MySQL 8.0

Authentication: JWT (PyJWT)

Data Formats: JSON, XML

Database ORM: Flask-MySQLdb

Installation
Prerequisites
Python 3.8+

MySQL 8.0+

pip (Python package manager)

Step 1: Clone and Setup
bash
# Clone the repository
git clone <repository-url>
cd student-management-api

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
Step 2: Install Dependencies
bash
pip install -r requirements.txt
If requirements.txt doesn't exist, install manually:

bash
pip install flask flask-mysqldb PyJWT
Step 3: Database Setup
Start MySQL server

Create database:

sql
CREATE DATABASE new_schema;
-- Or use your preferred database name
Step 4: Configuration
Update database credentials in application.py if needed:

python
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'  # Change to your MySQL password
app.config['MYSQL_DB'] = 'new_schema'  # Change to your database name
Step 5: Run the Application
bash
python application.py
The server will start at: http://localhost:5000

API Documentation
Authentication
Login
http
POST /login
Basic Auth Required: username=admin, password=admin123

Response:

json
{
    "message": "Login successful",
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "user": "admin"
}
Note: Use the received token in the Authorization header for protected endpoints:

text
Authorization: Bearer <your_token>
Student Endpoints
1. Get All Students
http
GET /students
Query Parameters:

search - Search by name, email, or student ID

major - Filter by major

year - Filter by enrollment year

min_gpa - Filter by minimum GPA

format - Response format (json or xml), default: json

Example Requests:

bash
# Get all students
curl http://localhost:5000/students

# Search for students named "John"
curl "http://localhost:5000/students?search=John"

# Get Computer Science students
curl "http://localhost:5000/students?major=Computer%20Science"

# Get 2024 students with GPA >= 3.5
curl "http://localhost:5000/students?year=2024&min_gpa=3.5"

# Get response in XML format
curl "http://localhost:5000/students?format=xml"
2. Get Single Student
http
GET /students/{id}
Path Parameter: id - Student's database ID

Example:

bash
curl http://localhost:5000/students/1
3. Create Student (Authenticated)
http
POST /students
Headers:

Authorization: Bearer <token>

Content-Type: application/json

Required Fields:

student_id (unique)

first_name

last_name

date_of_birth (YYYY-MM-DD)

gender (Male/Female/Other)

email (unique)

enrollment_year

Optional Fields:

phone

address

major

gpa

Example:

bash
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": "S2024011",
    "first_name": "Robert",
    "last_name": "Wilson",
    "date_of_birth": "2002-09-15",
    "gender": "Male",
    "email": "robert.wilson@university.edu",
    "major": "Computer Science",
    "enrollment_year": 2024,
    "gpa": 3.88
  }' \
  http://localhost:5000/students
4. Update Student (Authenticated)
http
PUT /students/{id}
Update specific fields of a student record.

Example:

bash
curl -X PUT \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "gpa": 3.92,
    "phone": "555-0121"
  }' \
  http://localhost:5000/students/1
5. Delete Student (Authenticated)
http
DELETE /students/{id}
Example:

bash
curl -X DELETE \
  -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:5000/students/5
Utility Endpoints
Health Check
http
GET /health
Check API and database status.

Response:

json
{
  "status": "healthy",
  "database": "connected",
  "student_count": 20
}
Statistics Dashboard
http
GET /stats
Get comprehensive statistics about students.

Response Includes:

Total student count

Average GPA

Distribution by major

Distribution by enrollment year

Distribution by gender

Top 5 students by GPA

Example:

bash
curl http://localhost:5000/stats
List All Majors
http
GET /majors
Get unique list of all academic majors.

Example:

bash
curl http://localhost:5000/majors
API Root
http
GET /
Get API information and available endpoints.

Database Schema
Students Table
sql
CREATE TABLE students (
    id INT PRIMARY KEY AUTO_INCREMENT,
    student_id VARCHAR(20) UNIQUE NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    date_of_birth DATE NOT NULL,
    gender ENUM('Male', 'Female', 'Other') NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    address TEXT,
    major VARCHAR(100),
    enrollment_year INT NOT NULL,
    gpa DECIMAL(3,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
Sample Student Data
The system comes pre-loaded with 20 sample students across various:

Majors: Computer Science, Biology, Engineering, Nursing, etc.

Years: 2022, 2023, 2024 enrollment years

GPAs: Range from 3.45 to 3.95

Demographics: Diverse names, locations, and genders

Response Formats
JSON Format (Default)
json
{
  "students": [
    {
      "id": 1,
      "student_id": "S2024001",
      "first_name": "John",
      "last_name": "Smith",
      "full_name": "John Smith",
      "date_of_birth": "2002-03-15",
      "gender": "Male",
      "email": "john.smith@university.edu",
      "phone": "555-0101",
      "address": "123 Main St, New York, NY",
      "major": "Computer Science",
      "enrollment_year": 2024,
      "gpa": 3.75,
      "created_at": "2024-01-15 10:30:00"
    }
  ],
  "count": 1,
  "message": "Success"
}
XML Format
Add ?format=xml to any GET request:

xml
<?xml version="1.0" ?>
<response>
  <students>
    <item>
      <id>1</id>
      <student_id>S2024001</student_id>
      <first_name>John</first_name>
      <last_name>Smith</last_name>
      <full_name>John Smith</full_name>
      <date_of_birth>2002-03-15</date_of_birth>
      <gender>Male</gender>
      <email>john.smith@university.edu</email>
      <phone>555-0101</phone>
      <address>123 Main St, New York, NY</address>
      <major>Computer Science</major>
      <enrollment_year>2024</enrollment_year>
      <gpa>3.75</gpa>
      <created_at>2024-01-15 10:30:00</created_at>
    </item>
  </students>
  <count>1</count>
  <message>Success</message>
</response>
Error Handling
The API provides informative error responses:

Common HTTP Status Codes
200 OK - Successful request

201 Created - Resource created successfully

400 Bad Request - Invalid input/data

401 Unauthorized - Missing or invalid token

404 Not Found - Resource doesn't exist

409 Conflict - Duplicate student_id or email

500 Internal Server Error - Server-side error

Error Response Format
json
{
  "error": "Detailed error message here"
}
Testing the API
Quick Test with cURL
bash
# 1. Get API info
curl http://localhost:5000/

# 2. Check health
curl http://localhost:5000/health

# 3. Get all students
curl http://localhost:5000/students

# 4. Get statistics
curl http://localhost:5000/stats

# 5. Login and save token
TOKEN=$(curl -s -u admin:admin123 -X POST http://localhost:5000/login | python -c "import sys, json; print(json.load(sys.stdin)['token'])")

# 6. Create new student with token
curl -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"student_id":"S2024012","first_name":"Test","last_name":"Student","date_of_birth":"2003-01-01","gender":"Other","email":"test@university.edu","enrollment_year":2024}' \
  http://localhost:5000/students
Testing with Postman
Import the following collection:

Base URL: http://localhost:5000

Create environment variable token for JWT

Test flow:

POST /login with Basic auth

Save token to environment

Use token in subsequent requests

Project Structure
text
student-management-api/
├── application.py          # Main Flask application
├── requirements.txt        # Python dependencies
├── README.md              # This documentation
└── venv/                  # Virtual environment
Dependencies
Main dependencies in requirements.txt:

text
Flask==2.3.3
Flask-MySQLdb==1.0.1
PyJWT==2.8.0
mysqlclient==2.2.0
Troubleshooting
Common Issues
MySQL Connection Error

text
Check: MySQL server is running
Solution: sudo service mysql start (Linux/Mac) or start MySQL service (Windows)
Module Not Found Error

text
Check: Virtual environment is activated
Solution: Run `pip install -r requirements.txt`
Access Denied for MySQL User

text
Check: MySQL credentials in application.py
Solution: Update with correct username/password
Port Already in Use

text
Check: Another service using port 5000
Solution: Change port in app.run(port=5001)
Debug Mode
For development, enable debug mode in application.py:

python
if __name__ == '__main__':
    app.run(debug=True, port=5000)
Security Considerations
Change Default Credentials

Update admin/admin123 in production

Change JWT_SECRET_KEY to strong random string

Database Security

Use environment variables for credentials

Implement proper MySQL user permissions

Regular database backups

API Security

Implement rate limiting in production

Use HTTPS in production

Regular token secret rotation

Development
Adding New Features
Add new endpoints in application.py

Implement corresponding database queries

Add input validation

Update documentation

Database Migrations
For schema changes:

Create migration scripts

Test with sample data

Backup before applying changes

License
MIT License - See LICENSE file for details.

Support
For issues and questions:

Check troubleshooting section

Review API documentation

Open an issue in the repository

Happy Coding! 🚀

This API provides a solid foundation for student management systems and can be extended for additional features like course enrollment, grades tracking, and faculty management.

