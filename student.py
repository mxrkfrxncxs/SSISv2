import course
import mysql.connector

db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="1234",
    database="ssisv2"
)

def check_IDNo(idNo):
    cursor = db.cursor()

    # Execute the query to check if idNo exists in the database
    query = "SELECT student_id FROM student_info WHERE student_id = %s"
    cursor.execute(query, (idNo,))
    result = cursor.fetchone()

    if result:
        return True
    else:
        return False

def check_ccode(course_code):
    cursor = db.cursor()

    query = "SELECT student_course FROM student_info WHERE LOWER(student_course) = LOWER(%s)"
    cursor.execute(query, (course_code,))
    result = cursor.fetchone()

    if result:
        return True
    else:
        return False


def add_student():
    cursor = db.cursor()

    idNo = input("Enter Student ID number: ")
    if check_IDNo(idNo) is True:
        print("Student", idNo, "already exists.\n")
    else:
        name = input("Enter Student's Name: ")
        gender = input("Enter Student's Gender: ")
        yr_level = input("Enter Student's Current Year Level: ")
        course_code = input("Enter Course Code (ex: BSCS for BS Computer Science): ")
        if not course.check_course(course_code):
            print("Student cannot be added.\n")
        else:
            query = "INSERT INTO student_info (student_id, student_name, student_gender, year_level, student_course) VALUES (%s, %s, %s, %s, %s)"
            values = (idNo, name, gender, yr_level, course_code)
            cursor.execute(query, values)
            db.commit()
            print("Student added successfully!\n")


def view_students():
    cursor = db.cursor()

    # Execute the query to fetch student data from the database
    query = "SELECT * FROM student_info"
    cursor.execute(query)
    data = cursor.fetchall()

    # Print the student data
    print("Course Code, Year Level, ID Number, Name, Gender")
    for row in data:
        print(row[4], row[3], row[0], "-", row[1], ",", row[2])
    print()


def delete_student():
    cursor = db.cursor()
    delIDNo = input("Enter Student ID number to be deleted: ")
    query = "DELETE FROM student_info WHERE student_id = %s"
    cursor.execute(query, (delIDNo,))
    db.commit()

    # Check if any rows were affected by the deletion
    if cursor.rowcount > 0:
        print("Student", delIDNo, "deleted successfully!\n")
    else:
        print("Student", delIDNo, "not found!\n")


def edit_student():
    cursor = db.cursor()

    # Execute the query to fetch student data from the database
    query = "SELECT * FROM student_info"
    cursor.execute(query)
    data = cursor.fetchall()

    idNo = input("Enter Student ID number to be edited: ")
    found = False
    for row in data:
        if row[0] == idNo:
            found = True
            print("Enter new student information:")
            new_name = input("Name: ") or row[1]
            new_gender = input("Gender: ") or row[2]
            new_yr_level = input("Year Level: ") or row[3]
            new_course_code = input("Course code: ") or row[4]
            if not course.check_course(new_course_code):
                print("Student Information cannot be edited.\n")
            else:
                query = "UPDATE student_info SET student_name = %s, student_gender = %s, year_level = %s, student_course = %s WHERE student_id = %s"
                values = (new_name, new_gender, new_yr_level, new_course_code, idNo)
                cursor.execute(query, values)
                db.commit()
                print("Student Information edited successfully.\n")
            break
    if not found:
        print("Student", idNo, "not found!\n")


def search_student():
    cursor = db.cursor()
    search_key = input("Enter Search Key: ")
    print()

    # Execute the query to search for students matching the search key
    query = "SELECT * FROM student_info WHERE student_id LIKE %s OR student_name LIKE %s OR student_gender LIKE %s OR year_level LIKE %s OR student_course LIKE %s"
    values = (f"%{search_key}%", f"%{search_key}%", f"%{search_key}%", f"%{search_key}%", f"%{search_key}%")
    cursor.execute(query, values)
    results = cursor.fetchall()

    if results:
        for row in results:
            print("ID Number: ", row[0])
            print("Student Name: ", row[1])
            print("Gender: ", row[2])
            print("Year Level: ", row[3])
            print("Course: ", row[4], "\n")
    else:
        print("Student not found.\n")
