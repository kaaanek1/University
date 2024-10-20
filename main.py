import sqlite3

db_connection = sqlite3.connect('university.db')
cursor = db_connection.cursor()

create_table_query = """ CREATE TABLE IF NOT EXISTS Students(
    id INT PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    department TEXT NOT NULL,
    date_of_birth DATETIME
)
"""
cursor.execute(create_table_query)


create_table_query = """ CREATE TABLE IF NOT EXISTS Teachers(
    teacher_id INT PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    surname TEXT NOT NULL,
    department TEXT NOT NULL
)
"""
cursor.execute(create_table_query)


create_table_query = """ CREATE TABLE IF NOT EXISTS Courses(
    course_id INT PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    teacher_id TEXT NOT NULL,
    FOREIGN KEY(teacher_id) REFERENCES Teachers(teacher_id)
)
"""
cursor.execute(create_table_query)


create_table_query = """ CREATE TABLE IF NOT EXISTS Exams(
    exam_id INT PRIMARY KEY AUTOINCREMENT,
    exam_data DATETIME,
    course_id INTEGER,
    max_score INTEGER,
    FOREIGN KEY (course_id) REFERENCES Courses(course_id)
)
"""
cursor.execute(create_table_query)


create_table_query = """ CREATE TABLE IF NOT EXISTS Grades(
    grade_id INT PRIMARY KEY AUTOINCREMENT,
    student_id INT,
    exam_id INT,
    score INT,
    FOREIGN KEY (student_id) REFERENCES Students(id),
    FOREIGN KEY (exam_id) REFERENCES Exams(exam_id)
)
"""
cursor.execute(create_table_query)

#Добавление инфы
def add_student(name, department, date_of_birth):
    cursor.execute("INSERT INTO Students (name, department, date_of_birth) VALUES (?, ?, ?)", (name, department, date_of_birth))
    db_connection.commit()


def add_teacher(name, surname, department):
    cursor.execute("INSERT INTO Teachers (name, surname, department) VALUES (?, ?, ?)", (name, surname, department))
    db_connection.commit()


def add_course(title, description, teacher_id):
    cursor.execute("INSERT INTO Courses (title, description, teacher_id) VALUES (?, ?, ?)", (title, description, teacher_id))
    db_connection.commit()


def add_exam(exam_data, course_id, max_score):
    cursor.execute("INSERT INTO Exams (exam_data, course_id, max_score) VALUES (?, ?, ?)", (exam_data, course_id, max_score))
    db_connection.commit()


def add_grade(student_id, exam_id, score):
    cursor.execute("INSERT INTO Grades (student_id, exam_id, score) VALUES (?, ?, ?)", (student_id, exam_id, score))
    db_connection.commit()


#Удаление инфы
def delete_student(id):
     cursor.execute("DELETE FROM Students WHERE id = ?", (id))
     db_connection.commit()

def delete_teacher(teacher_id):
    cursor.execute("DELETE FROM Teachers WHERE teacher_id = ?", (teacher_id))
    db_connection.commit()

def delete_course(course_id):
    cursor.execute("DELETE FROM Courses WHERE course_id = ?", (course_id))
    db_connection.commit()

def delete_exam(exam_id):
    cursor.execute("DELETE FROM Exams WHERE exam_id = ?", (exam_id))
    db_connection.commit()

#Обновление инфы
def update_student(id, name=None, department=None, date_of_birth=None):
    if name:
        cursor.execute("UPDATE Students SET name = ? WHERE id = ?", (name, id))
    if department:
        cursor.execute("UPDATE Students SET department = ? WHERE id = ?", (department, id))
    if date_of_birth:
        cursor.execute("UPDATE Students SET date_of_birth = ? WHERE id = ?", (date_of_birth, id))
    db_connection.commit()

def update_teacher(teacher_id, name=None, surname=None, department=None):
    if name:
        cursor.execute("UPDATE Teachers SET name = ? WHERE teacher_id = ?", (name, teacher_id))
    if department:
        cursor.execute("UPDATE Teachers SET department = ? WHERE teacher_id = ?", (department, teacher_id))
    if surname:
        cursor.execute("UPDATE Teachers SET surname = ? WHERE teacher_id = ?", (surname, teacher_id))
    db_connection.commit()

def update_course(course_id, title=None, description=None):
    if title:
        cursor.execute("UPDATE Courses SET title = ? WHERE course_id = ?", (title, course_id))
    if description:
        cursor.execute("UPDATE Courses SET description = ? WHERE course_id = ?", (description, course_id))
    db_connection.commit()


def get_students_in_course(name):
        cursor.execute("""
        SELECT name 
        FROM Students
        WHERE department = ?""", (name))
        return cursor.fetchall()



while True:
    print("Выберите действие")
    print("1-Добавить")
    print("2-Удалить")
    print("3-Изменить")
    print("4-Получить список")
    print("5-Средний балл")
    choice = int(input())

    if choice == 1:
        print("Что/кого добавить?")
        print("1-Ученика")
        print("2-Преподавателя")
        print("3-Курс")
        print("4-Оценку")
        print("5-Экзамен")
        obj = int(input())
        if obj == 1:
            name = input('Имя и фамилия: ')
            department = input("Факультет: ")
            date_of_birth = input("Дата рождения: ")
            add_student(name, department, date_of_birth)
        elif obj == 2:
            name = input("Имя: ")
            surname = input("Фамилия: ")
            department = input("Факультет: ")
            add_teacher(name, surname, department)
        elif obj == 3:
            title = input("Название: ")
            description = input("Описание: ")
            teacher_id = int(input("ID учителя: "))
            add_course(title, description, teacher_id)
        elif obj == 4:
            student_id = int(input("ID ученика: "))
            exam_id = int(input("ID экзамена: "))
            score = int(input("Оценка: "))
            add_grade(student_id, exam_id, score)
        else:
            exam_data = input("Дата экзамена: ")
            course_id = int(input("ID курса: "))
            max_score = int(input("Макс. балл: "))


    elif choice == 2:
        print("Что/кого удалить?")
        print("1-Ученика")
        print("2-Преподавателя")
        print("3-Курс")
        print("4-Экзамен")
        obj = int(input())
        if obj == 1:
            id = int(input('ID ученика: '))
            delete_student(id)
        elif obj == 2:
            teacher_id = int(input('ID учителя: '))
            delete_teacher(teacher_id)
        elif obj == 3:
            course_id = int(input('ID курса: '))
            delete_course(course_id)
        else:
            exam_id = int(input("ID экзамена: "))
            delete_exam(exam_id)


    elif choice == 3:
        print("Что/кого изменить?")
        print("1-Ученика")
        print("2-Преподавателя")
        print("3-Курс")
        print("Нажимайте ENTER в случае пропуска параметра")
        obj = int(input())
        if obj == 1:
            id = int(input("ID ученика: "))
            name = input("Имя: ")
            if name == '':
                name = None
            department = input('Факультет: ')
            if department == '':
                department = None
            date_of_birth = input('Дата рождения:')
            if date_of_birth == '':
                date_of_birth = None
            update_student(id, name, department, date_of_birth)
        elif obj == 2:
            teacher_id = int(input('ID преподавателя:' ))
            name = input("Имя: ")
            if name == '':
                name = None
            surname = input("Фамилия: ")
            if surname == '':
                surname = None
            department = input("Факультет: ")
            if department == '':
                department = None
            update_teacher(teacher_id, name, surname, department)
        elif obj == 3:
            course_id = int(input("ID курса: "))
            title = input("Название: ")
            if title == '':
                title = None
            description = input('Описание:')
            if description == "":
                description = None
            update_course(course_id, title, description)


    elif choice == 4:
        course_id = int(input("ID курса: "))
        get_students_in_course(course_id)
    elif choice == 5:
        pass
    else:
        break