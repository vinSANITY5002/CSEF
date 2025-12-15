
from flask import Flask, request, jsonify, make_response
from flask_mysqldb import MySQL
import xml.etree.ElementTree as ET
import jwt
import datetime
from functools import wraps
import os

app = Flask(__name__)


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'new_schema'  
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)


JWT_SECRET_KEY = 'your-secret-key-change-me'


def init_database():
    """Initialize database with your table structure"""
    try:
        cur = mysql.connection.cursor()
        
       
        cur.execute("DROP TABLE IF EXISTS students")
        
        
        cur.execute("""
            CREATE TABLE IF NOT EXISTS students (
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
            )
        """)
        
        
        sample_students = [
            ('S2024001', 'John', 'Smith', '2002-03-15', 'Male', 'john.smith@university.edu', '555-0101', '123 Main St, New York, NY', 'Computer Science', 2024, 3.75),
            ('S2024002', 'Emma', 'Johnson', '2003-05-22', 'Female', 'emma.johnson@university.edu', '555-0102', '456 Oak Ave, Boston, MA', 'Biology', 2024, 3.90),
            ('S2024003', 'Michael', 'Williams', '2002-11-08', 'Male', 'michael.w@university.edu', '555-0103', '789 Pine Rd, Chicago, IL', 'Business Administration', 2024, 3.65),
            ('S2024004', 'Sophia', 'Brown', '2003-02-14', 'Female', 'sophia.brown@university.edu', '555-0104', '321 Elm St, Los Angeles, CA', 'Psychology', 2024, 3.88),
            ('S2024005', 'Daniel', 'Jones', '2002-07-30', 'Male', 'daniel.jones@university.edu', '555-0105', '654 Maple Dr, Houston, TX', 'Engineering', 2024, 3.45),
            ('S2024006', 'Olivia', 'Garcia', '2003-09-12', 'Female', 'olivia.garcia@university.edu', '555-0106', '987 Cedar Ln, Phoenix, AZ', 'Nursing', 2024, 3.92),
            ('S2024007', 'David', 'Miller', '2002-12-05', 'Male', 'david.miller@university.edu', '555-0107', '147 Walnut St, Philadelphia, PA', 'Economics', 2024, 3.70),
            ('S2024008', 'Ava', 'Davis', '2003-04-18', 'Female', 'ava.davis@university.edu', '555-0108', '258 Birch Rd, San Antonio, TX', 'Political Science', 2024, 3.82),
            ('S2024009', 'James', 'Rodriguez', '2002-08-25', 'Male', 'james.rodriguez@university.edu', '555-0109', '369 Spruce Ave, San Diego, CA', 'Mathematics', 2024, 3.95),
            ('S2024010', 'Isabella', 'Martinez', '2003-01-31', 'Female', 'isabella.martinez@university.edu', '555-0110', '741 Ash St, Dallas, TX', 'Chemistry', 2024, 3.78),
            ('S2023001', 'Ethan', 'Hernandez', '2001-06-19', 'Male', 'ethan.hernandez@university.edu', '555-0111', '852 Poplar Dr, San Jose, CA', 'Physics', 2023, 3.60),
            ('S2023002', 'Mia', 'Lopez', '2001-10-27', 'Female', 'mia.lopez@university.edu', '555-0112', '963 Willow Way, Austin, TX', 'Sociology', 2023, 3.85),
            ('S2023003', 'Alexander', 'Wilson', '2001-03-03', 'Male', 'alexander.wilson@university.edu', '555-0113', '159 Magnolia Ct, Jacksonville, FL', 'History', 2023, 3.72),
            ('S2023004', 'Charlotte', 'Anderson', '2001-07-14', 'Female', 'charlotte.anderson@university.edu', '555-0114', '753 Redwood Blvd, San Francisco, CA', 'English Literature', 2023, 3.89),
            ('S2023005', 'Benjamin', 'Thomas', '2001-11-09', 'Male', 'benjamin.thomas@university.edu', '555-0115', '357 Sequoia Rd, Columbus, OH', 'Art History', 2023, 3.55),
            ('S2022001', 'Amelia', 'Taylor', '2000-02-28', 'Female', 'amelia.taylor@university.edu', '555-0116', '951 Sycamore Ln, Charlotte, NC', 'Music', 2022, 3.80),
            ('S2022002', 'William', 'Moore', '2000-09-07', 'Male', 'william.moore@university.edu', '555-0117', '852 Chestnut St, Fort Worth, TX', 'Philosophy', 2022, 3.68),
            ('S2022003', 'Abigail', 'Jackson', '2000-12-15', 'Female', 'abigail.jackson@university.edu', '555-0118', '753 Hickory Dr, Indianapolis, IN', 'Communications', 2022, 3.91),
            ('S2022004', 'Lucas', 'Martin', '2000-04-23', 'Male', 'lucas.martin@university.edu', '555-0119', '654 Pineapple St, Seattle, WA', 'Environmental Science', 2022, 3.77),
            ('S2022005', 'Harper', 'Lee', '2000-08-11', 'Female', 'harper.lee@university.edu', '555-0120', '456 Mango Ave, Denver, CO', 'Public Health', 2022, 3.84)
        ]
        
        
        cur.executemany("""
            INSERT INTO students 
            (student_id, first_name, last_name, date_of_birth, gender, email, phone, address, major, enrollment_year, gpa) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, sample_students)
        
        mysql.connection.commit()
        cur.close()
        print("✅ Database initialized with 20 students")
    except Exception as e:
        print(f"⚠️ Database warning: {e}")


with app.app_context():
    init_database()


def generate_token(username):
    """Generate JWT token"""
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1),
            'iat': datetime.datetime.utcnow(),
            'sub': username
        }
        token = jwt.encode(payload, JWT_SECRET_KEY, algorithm='HS256')
        return token
    except Exception as e:
        raise e

def token_required(f):
    """JWT decorator"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
        
        if not token:
            return jsonify({'error': 'Token missing'}), 401
        
        try:
            jwt.decode(token, JWT_SECRET_KEY, algorithms=['HS256'])
        except:
            return jsonify({'error': 'Invalid token'}), 401
        
        return f(*args, **kwargs)
    return decorated

def dict_to_xml(data_dict, root_tag='response'):
    """Convert dictionary to XML"""
    def add_elements(parent, data):
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, (dict, list)):
                    child = ET.SubElement(parent, key)
                    add_elements(child, value)
                else:
                    child = ET.SubElement(parent, key)
                    child.text = str(value) if value is not None else ''
        elif isinstance(data, list):
            for item in data:
                if isinstance(item, dict):
                    child = ET.SubElement(parent, 'item')
                    add_elements(child, item)
                else:
                    child = ET.SubElement(parent, 'item')
                    child.text = str(item)
    
    root = ET.Element(root_tag)
    add_elements(root, data_dict)
    
   
    import xml.dom.minidom
    xml_str = ET.tostring(root, encoding='unicode')
    dom = xml.dom.minidom.parseString(xml_str)
    return dom.toprettyxml()


@app.route('/')
def home():
    return jsonify({
        "message": "Student Management API",
        "version": "2.0",
        "database": "Complete student records",
        "endpoints": {
            "GET /students": "Get all students",
            "GET /students/<id>": "Get specific student",
            "POST /students": "Create student",
            "PUT /students/<id>": "Update student",
            "DELETE /students/<id>": "Delete student",
            "POST /login": "Get JWT token",
            "GET /stats": "Get statistics"
        }
    })

@app.route('/health')
def health():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT COUNT(*) as count FROM students")
        count = cur.fetchone()['count']
        cur.close()
        return jsonify({
            "status": "healthy", 
            "database": "connected",
            "student_count": count
        })
    except Exception as e:
        return jsonify({"status": "unhealthy", "error": str(e)}), 500

@app.route('/login', methods=['POST'])
def login():
    auth = request.authorization
    if auth and auth.username == 'admin' and auth.password == 'admin123':
        token = generate_token(auth.username)
        return jsonify({
            "message": "Login successful",
            "token": token,
            "user": auth.username
        })
    return jsonify({"error": "Invalid credentials"}), 401

@app.route('/students', methods=['GET'])
def get_students():
    try:
        format_type = request.args.get('format', 'json')
        search = request.args.get('search', '')
        major = request.args.get('major', '')
        year = request.args.get('year', '')
        min_gpa = request.args.get('min_gpa', '')
        
        cur = mysql.connection.cursor()
        
        query = """
            SELECT id, student_id, first_name, last_name, 
                   date_of_birth, gender, email, phone, address, 
                   major, enrollment_year, gpa, created_at 
            FROM students WHERE 1=1
        """
        params = []
        
        if search:
            query += " AND (first_name LIKE %s OR last_name LIKE %s OR email LIKE %s OR student_id LIKE %s)"
            params.extend([f'%{search}%', f'%{search}%', f'%{search}%', f'%{search}%'])
        
        if major:
            query += " AND major = %s"
            params.append(major)
        
        if year:
            query += " AND enrollment_year = %s"
            params.append(year)
        
        if min_gpa:
            query += " AND gpa >= %s"
            params.append(float(min_gpa))
        
        query += " ORDER BY enrollment_year DESC, last_name ASC"
        
        cur.execute(query, params)
        rows = cur.fetchall()
        cur.close()
        
        students = []
        for row in rows:
            students.append({
                'id': row['id'],
                'student_id': row['student_id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'full_name': f"{row['first_name']} {row['last_name']}",
                'date_of_birth': row['date_of_birth'].strftime('%Y-%m-%d') if row['date_of_birth'] else None,
                'gender': row['gender'],
                'email': row['email'],
                'phone': row['phone'],
                'address': row['address'],
                'major': row['major'],
                'enrollment_year': row['enrollment_year'],
                'gpa': float(row['gpa']) if row['gpa'] else None,
                'created_at': row['created_at'].strftime('%Y-%m-%d %H:%M:%S') if row['created_at'] else None
            })
        
        data = {
            'students': students,
            'count': len(students),
            'message': 'Success'
        }
        
        if format_type.lower() == 'xml':
            xml_response = dict_to_xml(data)
            response = make_response(xml_response)
            response.headers['Content-Type'] = 'application/xml'
            return response
        else:
            return jsonify(data)
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/students/<int:id>', methods=['GET'])
def get_student(id):
    try:
        format_type = request.args.get('format', 'json')
        
        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT id, student_id, first_name, last_name, 
                   date_of_birth, gender, email, phone, address, 
                   major, enrollment_year, gpa, created_at 
            FROM students WHERE id = %s
        """, (id,))
        row = cur.fetchone()
        cur.close()
        
        if not row:
            return jsonify({"error": "Student not found"}), 404
        
        student = {
            'id': row['id'],
            'student_id': row['student_id'],
            'first_name': row['first_name'],
            'last_name': row['last_name'],
            'full_name': f"{row['first_name']} {row['last_name']}",
            'date_of_birth': row['date_of_birth'].strftime('%Y-%m-%d') if row['date_of_birth'] else None,
            'gender': row['gender'],
            'email': row['email'],
            'phone': row['phone'],
            'address': row['address'],
            'major': row['major'],
            'enrollment_year': row['enrollment_year'],
            'gpa': float(row['gpa']) if row['gpa'] else None,
            'created_at': row['created_at'].strftime('%Y-%m-%d %H:%M:%S') if row['created_at'] else None
        }
        
        if format_type.lower() == 'xml':
            xml_response = dict_to_xml(student)
            response = make_response(xml_response)
            response.headers['Content-Type'] = 'application/xml'
            return response
        else:
            return jsonify(student)
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/students', methods=['POST'])
@token_required
def create_student():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
      
        required = ['student_id', 'first_name', 'last_name', 'date_of_birth', 'gender', 'email', 'enrollment_year']
        missing = [field for field in required if field not in data]
        if missing:
            return jsonify({"error": f"Missing required fields: {', '.join(missing)}"}), 400
        
        cur = mysql.connection.cursor()
        
        
        cur.execute("SELECT id FROM students WHERE student_id = %s OR email = %s", 
                   (data['student_id'], data['email']))
        if cur.fetchone():
            cur.close()
            return jsonify({"error": "Student ID or email already exists"}), 409
        
       
        cur.execute("""
            INSERT INTO students 
            (student_id, first_name, last_name, date_of_birth, gender, email, 
             phone, address, major, enrollment_year, gpa)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            data['student_id'],
            data['first_name'],
            data['last_name'],
            data['date_of_birth'],
            data['gender'],
            data['email'],
            data.get('phone'),
            data.get('address'),
            data.get('major'),
            data['enrollment_year'],
            data.get('gpa')
        ))
        
        mysql.connection.commit()
        student_id = cur.lastrowid
        cur.close()
        
        return jsonify({
            "message": "Student created successfully",
            "id": student_id,
            "student_id": data['student_id']
        }), 201
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/students/<int:id>', methods=['PUT'])
@token_required
def update_student(id):
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        cur = mysql.connection.cursor()
        
        
        cur.execute("SELECT id FROM students WHERE id = %s", (id,))
        if not cur.fetchone():
            cur.close()
            return jsonify({"error": "Student not found"}), 404
        
        
        if 'student_id' in data:
            cur.execute("SELECT id FROM students WHERE student_id = %s AND id != %s", 
                       (data['student_id'], id))
            if cur.fetchone():
                cur.close()
                return jsonify({"error": "Student ID already in use"}), 409
        
        if 'email' in data:
            cur.execute("SELECT id FROM students WHERE email = %s AND id != %s", 
                       (data['email'], id))
            if cur.fetchone():
                cur.close()
                return jsonify({"error": "Email already in use"}), 409
        
        
        allowed_fields = ['student_id', 'first_name', 'last_name', 'date_of_birth', 
                         'gender', 'email', 'phone', 'address', 'major', 
                         'enrollment_year', 'gpa']
        
        updates = []
        values = []
        for field in allowed_fields:
            if field in data:
                updates.append(f"{field} = %s")
                values.append(data[field])
        
        if not updates:
            cur.close()
            return jsonify({"error": "No valid fields to update"}), 400
        
        values.append(id)
        query = f"UPDATE students SET {', '.join(updates)} WHERE id = %s"
        
        cur.execute(query, values)
        mysql.connection.commit()
        cur.close()
        
        return jsonify({"message": "Student updated successfully"})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/students/<int:id>', methods=['DELETE'])
@token_required
def delete_student(id):
    try:
        cur = mysql.connection.cursor()
        
        
        cur.execute("SELECT student_id FROM students WHERE id = %s", (id,))
        student = cur.fetchone()
        if not student:
            cur.close()
            return jsonify({"error": "Student not found"}), 404
        
        cur.execute("DELETE FROM students WHERE id = %s", (id,))
        mysql.connection.commit()
        cur.close()
        
        return jsonify({
            "message": "Student deleted successfully",
            "deleted_student_id": student['student_id']
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/stats', methods=['GET'])
def get_statistics():
    """Get statistics about students"""
    try:
        cur = mysql.connection.cursor()
        
        
        cur.execute("SELECT COUNT(*) as total FROM students")
        total = cur.fetchone()['total']
        
        
        cur.execute("SELECT major, COUNT(*) as count FROM students GROUP BY major ORDER BY count DESC")
        majors = cur.fetchall()
        
        
        cur.execute("SELECT enrollment_year, COUNT(*) as count FROM students GROUP BY enrollment_year ORDER BY enrollment_year DESC")
        years = cur.fetchall()
        
       
        cur.execute("SELECT AVG(gpa) as avg_gpa FROM students WHERE gpa IS NOT NULL")
        avg_gpa = cur.fetchone()['avg_gpa']
        
      
        cur.execute("SELECT gender, COUNT(*) as count FROM students GROUP BY gender")
        genders = cur.fetchall()
        
        cur.execute("""
            SELECT student_id, first_name, last_name, gpa, major 
            FROM students 
            WHERE gpa IS NOT NULL 
            ORDER BY gpa DESC 
            LIMIT 5
        """)
        top_students = cur.fetchall()
        
        cur.close()
        
        stats = {
            "total_students": total,
            "average_gpa": round(float(avg_gpa), 2) if avg_gpa else None,
            "by_major": {row['major']: row['count'] for row in majors},
            "by_year": {str(row['enrollment_year']): row['count'] for row in years},
            "by_gender": {row['gender']: row['count'] for row in genders},
            "top_students": [
                {
                    'student_id': row['student_id'],
                    'name': f"{row['first_name']} {row['last_name']}",
                    'gpa': float(row['gpa']),
                    'major': row['major']
                }
                for row in top_students
            ]
        }
        
        return jsonify(stats)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/majors', methods=['GET'])
def get_majors():
    """Get list of all majors"""
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT DISTINCT major FROM students WHERE major IS NOT NULL ORDER BY major")
        rows = cur.fetchall()
        cur.close()
        
        majors = [row['major'] for row in rows]
        return jsonify({"majors": majors})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)