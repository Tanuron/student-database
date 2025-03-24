import mysql.connector
from mysql.connector import Error
import bcrypt
from getpass import getpass

class StudentManagementSystem:
    def __init__(self):
        self.connection = None
        self.cursor = None
        self.current_teacher = None
        
        try:
            self.connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='12345678',
                database='StudentDB'
            )
            if self.connection.is_connected():
                self.cursor = self.connection.cursor(dictionary=True)
        except Error as e:
            print(f"Error: {e}")
    def view_student_details(self, student_id):
        try:
            self.cursor.execute("""
            SELECT s.*, CONCAT(t.first_name, ' ', t.last_name) as created_by_name
            FROM Students s
            LEFT JOIN Teachers t ON s.created_by = t.teacher_id
            WHERE s.student_id = %s
            """, (student_id,))

            student = self.cursor.fetchone()

            if student:
                print("\n👨‍🎓 Student Details:")
                print(f"ID: {student['student_id']}")
                print(f"Name: {student['first_name']} {student['last_name']}")
                print(f"DOB: {student['date_of_birth']}")
                print(f"Address: {student['address']}")
                print(f"Phone: {student['phone']}")
                print(f"Email: {student['email']}")
                print(f"Major: {student['major']}")
                print(f"Enrollment Date: {student['enrollment_date']}")
                print(f"Created by: {student['created_by_name']}")
            else:
                print("⚠ Student not found.")
        except Error as e:
            print(f"Error: {e}")



    def teacher_login(self):
        username = input("Username: ")
        password = getpass("Password: ")
        
        try:
            self.cursor.execute("SELECT * FROM Teachers WHERE username = %s", (username,))
            teacher = self.cursor.fetchone()
            
            if teacher and bcrypt.checkpw(password.encode('utf-8'), teacher['password_hash'].encode('utf-8')):
                self.current_teacher = teacher
                print(f"Welcome, {teacher['first_name']} {teacher['last_name']}")
                return True
            else:
                print("❌ Invalid username or password")
                return False
        except Error as e:
            print(f"Error: {e}")
            return False

    def teacher_menu(self):
        while True:
            print("\n👨‍🏫 Teacher Menu:")
            print("1. Add New Student")
            print("2. View All Students")
            print("3. Add Course")
            print("4. Enroll Student in Course")
            print("5. Assign Grade")
            print("0. Logout")
            
            choice = input("Select option: ")
            
            if choice == '1':
                self.add_student()
            elif choice == '2':
                self.view_all_students()
            elif choice == '3':
                self.add_course()
            elif choice == '4':
                self.enroll_student()
            elif choice == '5':
                self.assign_grade()
            elif choice == '0':
                self.current_teacher = None
                break
            else:
                print("Invalid choice")

    def student_menu(self):
        while True:
            print("\n👨‍🎓 Student Menu:")
            print("1. View My Info")
            print("2. View My Courses")
            print("3. Calculate SGPA")  # Added SGPA Option
            print("0. Back")
            
            choice = input("Select option: ")
            
            if choice == '1':
                student_id = input("Enter your student ID: ")
                self.view_student_details(student_id)
            elif choice == '2':
                student_id = input("Enter your student ID: ")
                self.view_student_courses(student_id)
            elif choice == '3':
                student_id = input("Enter your student ID: ")
                self.calculate_sgpa(student_id)  # Call SGPA Calculation
            elif choice == '0':
                break
            else:
                print("Invalid choice")
    def assign_grade(self):
        """Assign a grade to a student for a specific course."""
        student_id = input("Enter Student ID: ")
        course_id = input("Enter Course ID: ")
        grade = input("Enter Grade (e.g., A, B, C, etc.): ")

        # Convert grade to grade points (assuming standard 4.0 scale)
        grade_points = {
            "A": 4.0, "A-": 3.7, "B+": 3.3, "B": 3.0, "B-": 2.7,
            "C+": 2.3, "C": 2.0, "C-": 1.7, "D+": 1.3, "D": 1.0, "F": 0.0
        }

        if grade not in grade_points:
            print("⚠ Invalid grade entered.")
            return

        try:
            self.cursor.execute("""
                UPDATE Enrollment 
                SET grade = %s, grade_point = %s
                WHERE student_id = %s AND course_id = %s
            """, (grade, grade_points[grade], student_id, course_id))

            self.connection.commit()
            print("✅ Grade assigned successfully!")
        except Error as e:
            print(f"Error: {e}")


    def calculate_sgpa(self, student_id):
        """Calculate and display SGPA for a student."""
        try:
            self.cursor.execute("""
                SELECT SUM(c.credits * e.grade_point) / SUM(c.credits) AS SGPA
                FROM Enrollment e
                JOIN Courses c ON e.course_id = c.course_id
                WHERE e.student_id = %s
                GROUP BY e.student_id;
            """, (student_id,))

            result = self.cursor.fetchone()

            if result and result['SGPA'] is not None:
                print(f"🎓 Student ID: {student_id}, SGPA: {round(result['SGPA'], 2)}")
            else:
                print("⚠ No grades found. SGPA cannot be calculated.")
        except Error as e:
            print(f"Error: {e}")

    def close_connection(self):
        if self.connection and self.connection.is_connected():
            self.cursor.close()
            self.connection.close()

def main():
    system = StudentManagementSystem()
    
    try:
        while True:
            print("\n🏫 Student Management System")
            print("1. Teacher Login")
            print("2. Student Access")
            print("0. Exit")
            
            choice = input("Select option: ")
            
            if choice == '1':
                if system.teacher_login():
                    system.teacher_menu()
            elif choice == '2':
                system.student_menu()
            elif choice == '0':
                break
            else:
                print("Invalid choice")
    finally:
        system.close_connection()

if __name__ == "__main__":
    main()
