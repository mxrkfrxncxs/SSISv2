import student
import mysql.connector

db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="1234",
    database="ssisv2"
)

def check_course(course_code):
    cursor = db.cursor()

    # Execute the query to check if course_code exists in the database
    query = "SELECT course_code FROM course WHERE LOWER(course_code) = LOWER(%s)"
    cursor.execute(query, (course_code,))
    result = cursor.fetchone()
    if result:
        return True
    else:
        # Prompt user to add the course if it doesn't exist in the database
        while True:
            print("Course not found in the database. Do you want to add it?\n[1] Yes\n[2] No")
            option = input("Enter your choice (1 or 2): ")
            if option == '1':
                add_course2(course_code)  # Replace with your function to add the course to the database
                return True
            elif option == '2':
                break

    return False

def add_course():
    cursor = db.cursor()

    course_already_added = False
    course_code = input("Enter Course Code (ex: BSCS for BS Computer Science): ")

    # Execute the query to check if course_code exists in the database
    query = "SELECT course_code FROM course WHERE LOWER(course_code) = LOWER(%s)"
    cursor.execute(query, (course_code,))
    result = cursor.fetchone()

    if result:
        print("Course", course_code.upper(), "already added!\n")
        course_already_added = True
    else:
        add_course2(course_code)  # Call the function to add the course to the database

    if not course_already_added:
        print("Course added successfully!\n")


def add_course2(course_code):
    cursor = db.cursor()

    course_title = input("Enter Course Title (ex: BS Computer Science for BSCS): ")

    # Execute the query to insert the course into the database
    query = "INSERT INTO course (course_code, course_title) VALUES (%s, %s)"
    values = (course_code.upper(), course_title)
    cursor.execute(query, values)
    db.commit()


def view_course():
    cursor = db.cursor()

    query = "SELECT * FROM course"
    cursor.execute(query)
    data = cursor.fetchall()

    # Print the student data
    print("Course Code, Course Title")
    for row in data:
        print(row[0], "-", row[1])
    print()

def edit_course():
    cursor = db.cursor()

    # Execute the query to fetch course data from the database
    query = "SELECT * FROM course"
    cursor.execute(query)
    data = cursor.fetchall()

    ccode = input("Enter Course Code to be edited: ")
    found = False
    for row in data:
        if row[0].upper() == ccode.upper():
            found = True
            new_course_title = input("Enter new Course Title (ex: BS Computer Science for BSCS): ") or row[1]
            query = "UPDATE course SET course_title = %s WHERE course_code = %s"
            values = (new_course_title, ccode.upper())
            cursor.execute(query, values)
            db.commit()
            print("Course", ccode.upper(), "edited successfully.\n")
            break
    if not found:
        print("Course", ccode.upper(), "not found!\n")


def delete_course():
    cursor = db.cursor()

    delCourseCode = input("Enter Course Code to be deleted: ")

    query = "SELECT course_code FROM course WHERE LOWER(course_code) = LOWER(%s)"
    cursor.execute(query, (delCourseCode,))
    result = cursor.fetchone()

    if result:
        while True:
            print("Are you sure to delete this course? Students under this course will also be deleted.\n[1] Yes\n[2] No")
            option = input("Enter your choice (1-2): ")
            if option == '1':
                if student.check_ccode(delCourseCode) is True:
                    student.deleteByCourse(delCourseCode)
                delete_query = "DELETE FROM course WHERE LOWER(course_code) = LOWER(%s)"
                cursor.execute(delete_query, (delCourseCode,))
                db.commit()
                print("Course", delCourseCode.upper(), "deleted successfully.\n")
                break
            elif option == '2':
                print("Course", delCourseCode.upper(), "not deleted.\n")
                break
            else:
                print("Invalid choice.\n")
    else:
        print("Course", delCourseCode.upper(), "not found!\n")


def search_course():
    cursor = db.cursor()
    search_key = input("Enter Search Key: ")
    print()

    # Execute the query to search for students matching the search key
    query = "SELECT * FROM course WHERE course_code LIKE %s OR course_title LIKE %s"
    values = (f"%{search_key}%", f"%{search_key}%")
    cursor.execute(query, values)
    results = cursor.fetchall()

    if results:
        found = True
        for row in results:
            print("Course Code: ", row[0])
            print("Course Title: ", row[1], "\n")
    else:
        found = False
        print("Course not found.\n")