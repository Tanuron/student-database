import mysql.connector
from mysql.connector import Error
import bcrypt

class DatabaseSetup:
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='12345678'
            )
            
            if self.connection.is_connected():
                self.cursor = self.connection.cursor()
                self.create_database()
                self.connection.database = "StudentDB"
                self.create_tables()
                self.insert_initial_data()
                print("✅ Database setup completed successfully")

        except Error as e:
            print(f"❌ Error: {e}")

    def create_database(self):
        self.cursor.execute("CREATE DATABASE IF NOT EXISTS StudentDB")

    def create_tables(self):
        # Teachers table with authentication
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Teachers (
                teacher_id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                first_name VARCHAR(50) NOT NULL,
                last_name VARCHAR(50) NOT NULL,
                department VARCHAR(50),
                email VARCHAR(100)
            )
        """)
        
        # Students table (no authentication)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Students (
                student_id INT AUTO_INCREMENT PRIMARY KEY,
                first_name VARCHAR(50) NOT NULL,
                last_name VARCHAR(50) NOT NULL,
                date_of_birth DATE,
                address VARCHAR(100),
                phone VARCHAR(20),
                email VARCHAR(100),
                major VARCHAR(50),
                enrollment_date DATE ,
                created_by INT,
                FOREIGN KEY (created_by) REFERENCES Teachers(teacher_id)
            )
        """)
        
        # Courses table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Courses (
                course_id INT AUTO_INCREMENT PRIMARY KEY,
                course_code VARCHAR(20) UNIQUE NOT NULL,
                course_name VARCHAR(100) NOT NULL,
                credits INT DEFAULT 3,
                teacher_id INT,
                FOREIGN KEY (teacher_id) REFERENCES Teachers(teacher_id)
            )
        """)
        
        # Enrollment table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Enrollment (
                enrollment_id INT AUTO_INCREMENT PRIMARY KEY,
                student_id INT,
                course_id INT,
                grade VARCHAR(2),
                FOREIGN KEY (student_id) REFERENCES Students(student_id),
                FOREIGN KEY (course_id) REFERENCES Courses(course_id)
            )
        """)
        
        self.connection.commit()
    

    def insert_initial_data(self):
        # Create default teacher account
        hashed_pw = bcrypt.hashpw("teacher123".encode('utf-8'), bcrypt.gensalt())
        
        self.cursor.execute("""
            INSERT INTO Teachers 
            (username, password_hash, first_name, last_name, department, email)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, ("teacher", hashed_pw.decode('utf-8'), "John", "Smith", "Computer Science", "teacher@school.edu"))
        
        # Sample student
        self.cursor.execute("""
            INSERT INTO Students 
            (first_name, last_name, date_of_birth, address, phone, email, major, created_by)
            VALUES (%s, %s, %s, %s, %s, %s, %s, 1)
        """, ("Alice", "Johnson", "2000-05-15", "123 Main St", "555-1234", "alice@school.edu", "Computer Science"))
        
        self.connection.commit()

    def close_connection(self):
        if self.connection.is_connected():
            self.cursor.close()
            self.connection.close()

if __name__ == "__main__":
    db = DatabaseSetup()
    db.close_connection()