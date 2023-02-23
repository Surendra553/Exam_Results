from django.http import HttpResponse
from django.shortcuts import render
# import sqlalchemy
from django.shortcuts import render
import pandas as pd
# import pymysql
import math
import mysql
from django.template import loader
from mysql.connector import cursor


def home(request):
    return render(request, "Home.html")

def Admin_Home(request):
    return render(request, "Admin.html")


# Create your views here.

def upload(request):
    Points = 0
    Test_Number = 0
    Cut_Off = 0
    try:
        if request.method == "POST":
            d = request.POST
            for key, value in d.items():
                if key == "Test_Number":
                    Test_Number = value
                if key == "Cut_Off":
                    Cut_Off = value
                if key == "Add_Points":
                    Points = value
                if key== "doe":
                    DOE = value
            print(DOE)

            Test_Number = int(Test_Number)
            Cut_Off = int(Cut_Off)
            Add_Points = int(Points)

            file = request.FILES["myfile"]
            df = pd.read_csv(file)

            tn = "Test_" + str(Test_Number)
            tr = "Test" + str(Test_Number) + "_Result"
            tp = "Test" + str(Test_Number) + "_Points"
            ts = "Test" + str(Test_Number) + "_Status"
            conn = mysql.connector.connect(host="localhost", user="root", password="Suri@143", database="Exam_Project")
            crsr = conn.cursor()

            qry = "insert into test_dates values('"+tn+"','"+DOE+"');"
            crsr.execute(qry)



            qry1 = "alter table student_data add column " + tr + " integer(5) default 0 after Total_Points"
            crsr.execute(qry1)
            qry2 = "alter table student_data add column " + tp + " integer(5) default 0 after Total_Points"
            crsr.execute(qry2)
            qry3 = "alter table student_data add column " + ts + " varchar(5) default 0 after Total_Points"
            crsr.execute(qry3)
            qry4 = "select Roll_Number from student_data;"
            crsr.execute(qry4)

            rl = crsr.fetchall()
            rls = []
            for i in range(len(rl)):
                rls.append(rl[i][0])

            for i in range(len(df["marks"])):

                if df["Roll number "][i] in rls:
                    mrk = int(df["marks"][i])
                    qry1 = 'update student_data set ' + tr + '=' + tr + '+' + str(mrk) + ' where Roll_Number="' + df["Roll number "][i] + '";'
                    crsr.execute(qry1)
                    if mrk >= Cut_Off:
                        qry2 = 'update student_data set ' + tp + '=' + tp + '+' + str(Add_Points) + ' where Roll_Number="' + df["Roll number "][i] + '";'
                        crsr.execute(qry2)
                        conn.commit()
                        qry3 = 'update student_data set ' + ts + '="PASS" where Roll_Number="' + df["Roll number "][i] + '";'
                        crsr.execute(qry3)
                        qry4 = "select * from student_data where Roll_Number='" + df["Roll number "][i] + "';"
                        crsr.execute(qry4)
                        rows = crsr.fetchall()
                        if rows[0][2] < 0:  # rows[0][2]=Streak
                            qry5 = "update student_data set Streak=1 where Roll_Number='" + df["Roll number "][i] + "';"
                            crsr.execute(qry5)

                        else:  # rows[0][3]=Points
                            qry5 = "update student_data set Streak=" + str(rows[0][2] + 1) + " where Roll_Number='" + df["Roll number "][i] + "';"
                            crsr.execute(qry5)
                        qry6 = "update student_data set Total_Points=" + str(rows[0][3] + Add_Points) + " where Roll_Number='" + df["Roll number "][i] + "';"
                        crsr.execute(qry6)


                        if rows[0][2] > 0 and rows[0][2] % 5 == 0:  # This is for adding Bonus
                            times = rows[0][2] // 5
                            bonus = math.ceil((rows[0][3]) * (times / 4))
                            qry7 = "update student_data set Total_Points=" + str(
                                rows[0][3] + bonus) + " where Roll_Number='" + df["Roll number "][i] + "';"
                            crsr.execute(qry7)

                    else:
                        qry2 = 'update student_data set ' + ts + '="FAIL" where Roll_Number="' + df["Roll number "][
                            i] + '";'
                        crsr.execute(qry2)
                        qry3 = "select * from student_data where Roll_Number='" + df["Roll number "][i] + "';"
                        crsr.execute(qry3)
                        rows = crsr.fetchall()
                        if rows[0][2] > 0:
                            qry5 = "update student_data set Streak=-1 where Roll_Number='" + df["Roll number "][
                                i] + "';"
                            crsr.execute(qry5)
                        else:
                            qry5 = "update student_data set Streak=" + str(rows[0][2] - 1) + " where Roll_Number='" + \
                                   df["Roll number "][i] + "';"
                            crsr.execute(qry5)

                        if rows[0][2] < 0 and rows[0][2] % 4 == 0:  # rows[0][2]=Streak
                            times = abs(rows[0][2] // 4)
                            fine = times * 20
                            qry6 = "update student_data set Total_Points=" + str(
                                rows[0][3] - fine) + " where Roll_Number='" + df["Roll number "][i] + "';"
                            crsr.execute(qry6)
            conn.commit()
            return render(request, "Success.html")
        else:
            return render(request, "Upload.html")

    except:
        return render(request, "Failure.html")
