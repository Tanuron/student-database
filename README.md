Student Management System

📌 Overview

This project is a Student Management System built using Python and MySQL. It allows teachers to manage students, courses, and grades, while students can access their information and calculate their SGPA.

🚀 Features Implemented So Far

✅ Database Connectivity

Established a connection to MySQL database (StudentDB).

Used mysql.connector for executing queries.

✅ Teacher Functionalities

Login system for teachers with bcrypt-based password hashing.

Teacher Menu with options to:

Add new students

View all students

Add courses

Enroll students in courses

Assign grades (In Progress - Method assign_grade just added)

✅ Student Functionalities

Student Menu with options to:

View personal details (view_student_details method implemented)

View enrolled courses (view_student_courses method required)

Calculate SGPA (calculate_sgpa method implemented)

🔧 Features Still Needed

Implement assign_grade() for assigning grades to students.

Implement view_student_courses() to display courses a student is enrolled in.

Improve error handling and validations.

Create a student login system (currently, students enter their IDs manually).

🛠 Technologies Used

Python (for backend logic)

MySQL (database management)

bcrypt (password hashing)

getpass (for secure password input)

📝 Next Steps

Complete assign_grade() and view_student_courses() methods.

Implement a student authentication system.

Improve user experience with better prompts and validations.

Build a frontend interface (Optional).

🚀 Project is progressing well! Keep improving it with more features.
