import sqlite3


def create_database(fun):
    def wrapper(*args, **kwargs):
        connection = sqlite3.connect("grades.sqlite3")
        cursor = connection.cursor()
        command = """ CREATE TABLE IF NOT EXISTS subject_list (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT UNIQUE);"""
        command_2 = """CREATE TABLE IF NOT EXISTS grades (
            subject_name TEXT,
            grade REAL,
            date INTEGER,
            weight REAL,
            type TEXT);"""
        cursor.execute(command)
        cursor.execute(command_2)
        connection.commit()
        connection.close()
        
        result = fun(*args, **kwargs)

        return result
    return wrapper
    

@create_database
def add_subject(subject: str):
    command = f"INSERT INTO subject_list (subject) VALUES ('{subject.upper()}');"
    try:
        connection = sqlite3.connect("grades.sqlite3")
        cursor = connection.cursor()
        cursor.execute(command)
        connection.commit()
        connection.close()
        return True
    except sqlite3.IntegrityError as e:
        print(e, command)
        return "duplicate subject"
    except Exception:
        return False


@create_database
def list_subjects():
    command = "SELECT * FROM subject_list"
    subject_list = []
    try:
        connection = sqlite3.connect("grades.sqlite3")
        cursor = connection.cursor()
        cursor.execute(command)
        for _,y in cursor:
            subject_list.append(y)
        connection.commit()
        connection.close()
        return subject_list
    except Exception as e:
        print(e)
        return subject_list


@create_database
def add_grade(subject_name, grade, date, weight, type):
    command = f"INSERT INTO grades (subject_name, grade, date, weight, type) VALUES ('{subject_name}', '{grade}', '{date}', '{weight}', '{type}')"
    try:
        connection = sqlite3.connect("grades.sqlite3")
        cursor = connection.cursor()
        cursor.execute(command)
        connection.commit()
        connection.close()
        return True
    except Exception as e:
        print(e, command)
        return False
    

@create_database
def list_grades(subject: str):
    command = f"SELECT * FROM grades WHERE subject_name = '{subject}'"
    grades_list = []
    try:
        connection = sqlite3.connect("grades.sqlite3")
        cursor = connection.cursor()
        cursor.execute(command)
        for _,x,y,z,a in cursor:
            grade_tuple = (x,y,z,a)
            grades_list.append(grade_tuple)
        connection.commit()
        connection.close()
        return grades_list
    except Exception as e:
        print(e)
        return grades_list


@create_database
def return_average(subject: str):
    command = f"SELECT SUM(grade*weight)/SUM(weight) AS average_grade FROM grades WHERE subject_name = '{subject}'"
    try:
        connection = sqlite3.connect("grades.sqlite3")
        cursor = connection.cursor()
        cursor.execute(command)
        average = cursor.fetchone()
        average_grade = average[0]
        connection.close()
        return f'{average_grade:.2f}'
    except Exception as e:
        print(e)
        return 'N/A'


@create_database
def return_averages():
    command = f"SELECT subject_name, SUM(grade*weight)/SUM(weight) AS average_grade FROM grades GROUP BY subject_name;"
    averages_list = []
    try:
        connection = sqlite3.connect("grades.sqlite3")
        cursor = connection.cursor()
        cursor.execute(command)
        averages = cursor.fetchall()
        for subject, average in averages:
            averages_tuple = (subject, round(average, 2))
            averages_list.append(averages_tuple)
        subjects = list_subjects()
        subjects_set = set(subjects)
        subjects_check = []
        for subject in averages_list:
            subjects_check.append(subject[0])
        subjects_check_set = set(subjects_check)
        subjects_to_add = (subjects_set-subjects_check_set)
        if len(subjects_to_add) == 0:
            connection.close()
            return averages_list
        else:
            for subject in subjects_to_add:
                subject_tuple = (subject, 'N/A')
                averages_list.append(subject_tuple)
            return averages_list
    except Exception as e:
        print(e, command)
        return averages_list


@create_database
def return_general_average():
    command = f"SELECT SUM(grade*weight)/SUM(weight) AS average_grade FROM grades;"
    try:
        connection = sqlite3.connect("grades.sqlite3")
        cursor = connection.cursor()
        cursor.execute(command)
        average = cursor.fetchone()
        general_average = average[0]
        connection.close()
        return f'{general_average:.2f}'
    except Exception as e:
        print(e)
        return 'N/A'
