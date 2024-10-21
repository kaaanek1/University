import sqlite3

db_connection = sqlite3.connect('univer.db')
cursor = db_connection.cursor()

create_table_query = """
CREATE TABLE IF NOT EXISTS Students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,  
    name TEXT NOT NULL,
    surname TEXT NOT NULL,
    department TEXT NOT NULL,
    date_of_birth DATETIME
)
"""
cursor.execute(create_table_query)


create_table_query = """ CREATE TABLE IF NOT EXISTS Teachers(
    teacher_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    surname TEXT NOT NULL,
    department TEXT NOT NULL
)
"""
cursor.execute(create_table_query)


create_table_query = """ CREATE TABLE IF NOT EXISTS Courses(
    course_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    teacher_id TEXT NOT NULL,
    FOREIGN KEY(teacher_id) REFERENCES Teachers(teacher_id)
)
"""
cursor.execute(create_table_query)


create_table_query = """ CREATE TABLE IF NOT EXISTS Exams(
    exam_id INTEGER PRIMARY KEY AUTOINCREMENT,
    exam_data DATETIME,
    course_id INTEGER,
    max_score INTEGER,
    FOREIGN KEY (course_id) REFERENCES Courses(course_id)
)
"""
cursor.execute(create_table_query)


create_table_query = """ CREATE TABLE IF NOT EXISTS Grades(
    grade_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INT,
    exam_id INT,
    score INT,
    FOREIGN KEY (student_id) REFERENCES Students(id),
    FOREIGN KEY (exam_id) REFERENCES Exams(exam_id)
)
"""
cursor.execute(create_table_query)

#Добавление инфы
def add_student(name, surname, department, date_of_birth):
    cursor.execute("INSERT INTO Students (name, surname, department, date_of_birth) VALUES (?, ?, ?, ?)", (name, surname, department, date_of_birth))
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
     cursor.execute(f"DELETE FROM Students WHERE id = {id}")
     db_connection.commit()

def delete_teacher(teacher_id):
    cursor.execute(f"DELETE FROM Teachers WHERE teacher_id = {teacher_id}")
    db_connection.commit()

def delete_course(course_id):
    cursor.execute(f"DELETE FROM Courses WHERE course_id = {course_id}")
    db_connection.commit()

def delete_exam(exam_id):
    cursor.execute(f"DELETE FROM Exams WHERE exam_id = {exam_id}")
    db_connection.commit()

#Обновление инфы
def update_student(id, name=None, surname = None, department=None, date_of_birth=None):
    if name:
        cursor.execute("UPDATE Students SET name = ? WHERE id = ?", (name, id))
    if surname:
        cursor.execute("UPDATE Students SET surname = ? WHERE id = ?", (surname, id))
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


def get_students_in_department(department):
    cursor.execute(f"SELECT id, name, surname FROM Students WHERE department = '{department}'")
    result = cursor.fetchall()
    print(f'Факультет "{department}"')
    for row in result:
        print(f'ID:{row[0]}----Имя:{row[1]}----Фамилия:{row[2]}')
    print('\n')


def get_teacher_courses(teacher_id):
    cursor.execute(f"SELECT course_id, title, description FROM Courses WHERE teacher_id = {teacher_id}")
    result = cursor.fetchall()
    print(f'Преподаватель с ID {teacher_id}')
    for row in result:
        print(f"ID курса:{row[0]}----Название:{row[1]}----Описание:{row[2]}")
    print("\n")


def get_grades(student_id):
    cursor.execute(f"SELECT exam_id, score FROM Grades WHERE student_id = {student_id}")
    result = cursor.fetchall()
    print(f"Успеваемость студента с ID {student_id}")
    for row in result:
        print(f"ID экзамена:{row[0]}----Оценка:{row[1]}")
    print("\n")

def average_student(student_id):
    cursor.execute(f"SELECT avg(score) FROM Grades WHERE student_id = {student_id}")
    res = cursor.fetchall()
    print(f"Средний балл студента с ID {student_id}: {res[0][0]}\n")

def average_of_department(department):
    cursor.execute(f"""SELECT avg(score)
        FROM Students s
        JOIN Grades g on s.id = g.student_id
        WHERE department = '{department}'""")
    res = cursor.fetchall()
    print(f"Средний балл по факультету {department}: {res[0][0]}\n")


while True:
    try:
        print("Выберите действие(для выхода ввести EX)")
        print("1-Добавить")
        print("2-Удалить")
        print("3-Изменить")
        print("4-Получить список")
        print("5-Средний балл")
        choice = input()
        print("\n")

        if choice == "1":
            print("Что/кого добавить?")
            print("1-Добавить студента")
            print("2-Добавить преподавателя")
            print("3-Добавить курс")
            print("4-Добавить оценку")
            print("5-Добавить экзамен")
            obj = input()
            print("\n")
            if obj == '1':
                name = input('Имя: ')
                surname = input('Фамилия: ')
                department = input("Факультет: ")
                date_of_birth = input("Дата рождения: ")
                add_student(name, surname, department, date_of_birth)
            elif obj == '2':
                name = input("Имя: ")
                surname = input("Фамилия: ")
                department = input("Факультет: ")
                add_teacher(name, surname, department)
            elif obj == '3':
                title = input("Название: ")
                description = input("Описание: ")
                teacher_id = int(input("ID преподавателя: "))
                add_course(title, description, teacher_id)
            elif obj == '4':
                student_id = int(input("ID студента: "))
                exam_id = int(input("ID экзамена: "))
                score = int(input("Оценка: "))
                add_grade(student_id, exam_id, score)
            elif obj == '5':
                exam_data = input("Дата экзамена: ")
                course_id = int(input("ID курса: "))
                max_score = int(input("Макс. балл: "))


        elif choice == "2":
            print("Что/кого удалить?")
            print("1-Удалить студента")
            print("2-Удалить преподавателя")
            print("3-Удалить курс")
            print("4-Удалить экзамен")
            obj = input()
            print("\n")
            if obj == "1":
                id = int(input('ID студента: '))
                delete_student(id)
                print("Студент успешно удален\n")
            elif obj == '2':
                teacher_id = int(input('ID преподавателя: '))
                delete_teacher(teacher_id)
                print("Преподаватель успешно удален\n")
            elif obj == '3':
                course_id = int(input('ID курса: '))
                delete_course(course_id)
                print("Курс успешно удален\n")
            elif obj == '4':
                exam_id = int(input("ID экзамена: "))
                delete_exam(exam_id)
                print("Экзамен успешно удален\n")


        elif choice == "3":
            print("Что/кого изменить?")
            print("1-Изменить ученика")
            print("2-Изменить преподавателя")
            print("3-Изменить курс")
            obj = input()
            print("\n")
            print("Нажимайте ENTER, если хотите оставить параметр прежним")
            if obj == '1':
                id = int(input("ID ученика: "))
                name = input("Имя: ")
                if name == '':
                    name = None
                surname = input('Фамилия: ')
                if surname == '':
                    surname = None
                department = input('Факультет: ')
                if department == '':
                    department = None
                date_of_birth = input('Дата рождения:')
                if date_of_birth == '':
                    date_of_birth = None
                update_student(id, name, surname, department, date_of_birth)
            elif obj == '2':
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
            elif obj == '3':
                course_id = int(input("ID курса: "))
                title = input("Название: ")
                if title == '':
                    title = None
                description = input('Описание:')
                if description == "":
                    description = None
                update_course(course_id, title, description)


        elif choice == "4":
            print("Какой список вывести?")
            print('1-Список студентов на факультете')
            print('2-Список курсов читаемых преподавателем')
            print('3-Список оценок студента')
            obj = input()
            print("\n")
            if obj == '1':
                dep_id = input("Название факультета: ")
                get_students_in_department(dep_id)
            elif obj == '2':
                teacher_id = int(input("ID преподавателя: "))
                get_teacher_courses(teacher_id)
            elif obj == '3':
                student_id = int(input("ID студента: "))
                get_grades(student_id)

        elif choice == "5":
            print("Какой средний балл вывести?")
            print("1-Средний балл студента в целом")
            print("2-Средний балл по факультету")
            obj = input()
            print("\n")
            if obj == '1':
                student_id = int(input("ID студента: "))
                average_student(student_id)
            elif obj == '2':
                department = input("Название факультета: ")
                average_of_department(department)

        elif choice == "EX" or choice == "ex":
            break
        else:
            print("Некорректный ввод, попробуйте еще раз\n")
    except:
        print("ОШИБКА!!! ВВЕДИ КОРРЕКТНЫЕ ДАННЫЕ\n")