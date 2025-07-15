import tkinter as tk
from tabulate import tabulate
import mysql.connector
import random

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Naethen_1912",
    database="quiz_db")
cursor = db.cursor()

qs_names = ['Questions', 'Answers', 'id']
col_names = ["Names", "Grade", "Section", "Marks"]

def addquestions():
    n = int(input('No. of Questions to be Added: '))
    for i in range(1, n + 1):
        qs = input('Enter Questions:')
        ans = input('Enter Answer:')
        cursor.execute("insert into questions (question_text, correct_answer) VALUES (%s, %s)", (qs, ans))
        db.commit()
    print('Questions added')

def showqs():
    cursor.execute('select * from questions')
    display = cursor.fetchall()
    m=tabulate(display, headers=qs_names, tablefmt="simple_grid")
    print(m)
    print('\n')

def get_questions():
    cursor.execute("select * from questions order by rand()")
    questions = cursor.fetchall()
    return questions

def del_questions():
    qno = int(input('The Question No. to be Deleted:'))
    query1 = "delete from questions where id = %s"
    cursor.execute(query1, (qno,))
    db.commit()
    query2 = 'alter table questions drop column id'
    cursor.execute(query2)
    db.commit() # If question is deleted from the middle of the table
    query3 = 'alter table questions add id INT AUTO_INCREMENT PRIMARY KEY'
    cursor.execute(query3)
    db.commit()
    print('Question Deleted')

def updateques():
    qno = int(input('The Question No. to be Updated:'))
    q = input('Enter New Question / Enter Old Question if not to be updated:')
    s = input('Enter New Answer / Enter Old Answer if not to be updated:')
    query = "update questions set question_text = %s, correct_answer = %s where id = %s"
    cursor.execute(query, (q, s, qno))
    db.commit()
    print('Question Updated Successfully')

def start_quiz():
    name = input("Enter your Name: ")
    grade= input("Enter your Grade: ")
    section= input('Enter your Section:')
    marks=0
    questions = get_questions()
    for question in questions:
        question_text, correct_answer, question_id = question
        print("Question:", question_text)
        user_answer = input("Your answer: ")
        if user_answer.lower() == correct_answer.lower():
            print("Correct!\n")
            marks+=1
        else:
            print("Incorrect. The correct answer is:", correct_answer, "\n")
    print("Quiz finished!", name, 'your marks:' ,marks)
    cursor.execute(
        "insert into user_profiles (name, grade,section, marks) VALUES ('{}','{}','{}','{}')".format(name,grade,section,marks))
    db.commit()

def display_profiles():
    cursor.execute("SELECT name, grade, section, marks FROM user_profiles")
    profiles = cursor.fetchall()
    print(tabulate(profiles, headers=col_names, tablefmt="simple_grid"))

def exportdata():
    query = "select * from user_profiles"
    cursor.execute(query)
    result = cursor.fetchall()
    file = "Output.txt"
    with open(file, "w") as file:
        for row in result:
            file.write(str(row) + "\n")
    print('Data exported \n')

def admin_menu():
    admin = tk.Tk()
    admin.geometry('925x500')
    admin.title("ADMIN")
    admin.configure(background='white')

    photo_image = tk.PhotoImage(file='login.png')
    L1=tk.Label(image=photo_image, background="white")
    L1.place(x=60, y=50)
    
    adminmenu = tk.Label(admin, text='Admin Options',foreground='light blue',background='white', font=('Courier New',23,'bold'))
    adminmenu.place(x=575,y=30)

    adminframe = tk.Frame(width=350, height=350, background='White')
    adminframe.place(x=520,y=70)

    addquestions_button = tk.Button(adminframe, text="Add Questions",fg='Black',bg='White',font = ('Courier New',14), command=addquestions)
    displayquestions_button = tk.Button(adminframe, text="Display Questions",fg='Black',bg='White',font = ('Courier New',14), command=showqs)
    deletequestions_button = tk.Button(adminframe, text="Delete Questions",fg='Black',bg='White',font = ('Courier New',14), command=del_questions)
    updatequestions_button = tk.Button(adminframe, text="Update Questions",fg='Black',bg='White',font = ('Courier New',14), command=updateques)
    display_button = tk.Button(adminframe, text="Display Leaderboard",fg='Black',bg='White',font = ('Courier New',14), command=display_profiles)
    exportdata_button = tk.Button(adminframe, text="Export Data",fg='Black',bg='White',font = ('Courier New',14), command=exportdata)
    exitbutton = tk.Button(adminframe, text="Exit",fg='Black',bg='White',font = ('Courier New',14), command=admin.destroy)

    addquestions_button.place(x=100,y=10)
    displayquestions_button.place(x=80,y=60)
    deletequestions_button.place(x=80,y=110)
    updatequestions_button.place(x=80,y=160)
    exportdata_button.place(x=105,y=210)
    display_button.place(x=65,y=260)
    exitbutton.place(x=140,y=305)

    admin.mainloop()

def student_menu():
    student= tk.Tk()
    student.geometry('900x500')
    student.title("USER")
    student.configure(background='white')

    photo_image = tk.PhotoImage(file='login.png')
    L1=tk.Label(image=photo_image, background="white")
    L1.place(x=60, y=50)

    studentlabel = tk.Label(student, text='User Options',foreground='light blue',background='white', font=('Courier New',23,'bold'))
    studentlabel.place(x=575,y=30)
    
    studentframe = tk.Frame(width=350, height=350, background='White')
    studentframe.place(x=520,y=70)
    

    startquiz_button = tk.Button(studentframe, text="Start Quiz",fg='Black',bg='White',font = ('Courier New',14), command=start_quiz)
    display_button = tk.Button(studentframe, text="Display Leaderboard",fg='Black',bg='White',font = ('Courier New',14), command=display_profiles)
    exit_button = tk.Button(studentframe, text="Exit",fg='Black',bg='White',font = ('Courier New',14), command=student.destroy)

    startquiz_button.place(x=100,y=30)
    display_button.place(x=50,y=80)
    exit_button.place(x=125,y=130)

    student.mainloop()

while True:
    print('1. Login as Admin')
    print('2. Login as Student')
    print('3. Exit')
    n = int(input('Enter your Choice:'))
    if n == 1:
        password = 'ADMIN'
        password1 = input('Enter password: ')
        if password1 == password:
            admin_menu()
        else:
            print('WRONG password. Please try again!\n')
    elif n == 2:
        student_menu()
    elif n == 3:
        print("Exiting the application.")
        break
    else:
        print('Invalid Choice. Please select a valid option')
db.close()
