from django.db.backends import mysql
from django.shortcuts import render
from mysql.connector import cursor
import mysql

# Create your views here.

def Student(request):
    return render(request, "Student.html")

def result(request):
        conn = mysql.connector.connect(host="localhost", user="root", password="Suri@143", database="Exam_Project")
        crsr = conn.cursor()
        qry = "select * from student_data;"
        crsr.execute(qry)
        all_data = crsr.fetchall()
        l = len(all_data)

        context = {
                'all_data' : all_data,
        }
        return render(request, "Student_Results.html",context)




def search(request):
    if request.method=="POST":
        d = request.POST
        for key, value in d.items():
            if key == "search":
                search = value
        conn = mysql.connector.connect(host="localhost", user="root", password="Suri@143", database="Exam_Project")
        crsr = conn.cursor()
        qry1 = "select * from student_data where Roll_Number like '%"+search+"%';"
        crsr.execute(qry1)
        data = crsr.fetchone()
        l = len(data)
        qry2 = "select Test_Date from test_dates;"
        crsr.execute(qry2)
        d = crsr.fetchall()     # d means dates
        d = d[::-1]
        qry3 = "select Test_Name from test_dates;"
        crsr.execute(qry3)
        n = crsr.fetchall()          #n means Test Name
        n = n[::-1]
        status = data[4:l-1:3]
        points = data[5:l-1:3]
        result = data[6:l:3]
        spr = []

        for i in range(len(status)):
            spr.append([n[i][0],status[i],points[i],result[i],str(d[i])[15:19]+"-"+str(d[i])[21:23]+"-"+str(d[i])[24:27]])
            if spr[i][4][10]==')':
                spr[i][4] = spr[i][4][:10]
        context = {
            'Name' : data[0],
            'Roll' : data[1],
            'Total_Points' : data[3],
            'Streak' : data[2],
            'spr' : spr

        }
    return render(request, "Search.html", context)




def fun(request):
    return render(request,"Search.html")