
import mysql.connector
from tabulate import *


#MODULE TO CHECK MYSQL CONNECTIVITY

def MYSQLconnectionCheck():

    # GLOBAL VARIABLES DECLARATION
    global myConnection
    global userName
    global password
    
    while True :
        userName = input("| Enter MYSQL Server's Name : ")
        if len(userName) >= 1 :
            password = input("| Entre MYSQL Server's password : ")
            if len(password) >= 1:
                break
            else:
                print("!!! INVALID INPUT !!!")
        else:
            print("!!! INVALID INPUT !!!")
    try :
        myConnection = mysql.connector.connect( host = "localhost" , user= userName , passwd = password , auth_plugin = "mysql_native_password")
    except:
        print("! ERROR ESTABLISHING MYSQL CONNECTION CHECK USERNAME AND PASSWORD !")
        print("--------------------------------------------------------------------")
        MYSQLconnectionCheck()
    if myConnection :
        print("CONGRATULATIONS ! YOUR MYSQL CONNECTION HAS BEEN ESTABLISHED !")
        cursor=myConnection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS SMS")
        cursor.execute("USE SMS")
        cursor.execute("COMMIT")
        cursor.close()
        return myConnection
    else:
        print("! ERROR ESTABLISHING MYSQL CONNECTION CHECK USERNAME AND PASSWORD !")

#MODULE TO ESTABLISHED MYSQL CONNECTION

def MYSQLconnection ():
    myConnection=mysql.connector.connect(host="localhost",user=userName,passwd =password , database="SMS" , auth_plugin='mysql_native_password' )
    if myConnection:
         return myConnection
    else:
        print("! ERROR ESTABLISHING MYSQL CONNECTION !")
        myConnection.close()

#MODULE FOR NEW ADMISSION

def newstudent():
    if myConnection:
        cursor = myConnection.cursor()
        createtable = """CREATE TABLE IF NOT EXISTS STUDENT(SNAME VARCHAR(30),FNAME VARCHAR(30),MNAME VARCHAR(30),PHONE VARCHAR(10),ADDRESS VARCHAR(100),SCLASS VARCHAR(3),SSECTION VARCHAR(1),SADMISSION_NO INT PRIMARY KEY AUTO_INCREMENT)"""
        cursor.execute(createtable)
        query = """ALTER TABLE STUDENT AUTO_INCREMENT=1001;"""
        cursor.execute(query)
        while True :
            sname = input("| Enter Student's Name : ").title()
            if (sname.replace(' ','')).isalpha() and len(sname) <= 30 : 
                break
            else:
                print("!!! INVALID INPUT !!!")
        while True :
            fname = input("| Enter Father's Name : ").title()
            if (fname.replace(" ","")).isalpha() and len(fname) <= 30 :
                break 
            else:
                print("!!! INVALID INPUT !!!")
        while True :
            mname = input("| Enter Mother's Name : ").title()
            if (mname.replace(' ','')).isalpha() and len(mname) <= 30 :
                break
            else:
                print("!!! INVALID INPUT !!!")
        while True :
            phone = input("| Enter Contact_no : " )
            if phone.isdigit() and len(phone) == 10 :
                break
            else:
                print("!!! INVALID INPUT !!!")
        while True :
            address = input("| Enter Address : " )
            if len(address.strip()) <= 100 :
                break 
            else:
                print("!!! INVALID INPUT !!!")
        while True :
            cls_name = {'@':'LKG','0':'UKG','1':'I','2':'II','3':'III','4':'IV','5':'V','6':'VI','7':'VII','8':'VIII','9':'IX','10':'X','11':'XI','12':'XII'}
            print(' -------------------------------')
            for x,y in cls_name.items():
                print('| PRESS ',x,' FOR ',y,' CLASS \t|')
                print(' -------------------------------')
                s_class = input("| Enter Class : " )
                if s_class in cls_name.keys():
                    sclass = cls_name[s_class]
                    sec = ('A','B','C')
                    print('-----')
                    for i in sec :
                        print('|',i,'|')
                        print('-----')
                else:
                    print("!!! INVALID INPUT !!!")
        while True :
            ssection = input("| Enter Section : ").title()
            if ssection in sec :
                break
            else:
                print("!!! INVALID INPUT !!!")
                                    
        sql = "INSERT INTO STUDENT(SNAME,FNAME,MNAME,PHONE,ADDRESS,SCLASS,SSECTION) VALUES(%s,%s,%s,%s,%s,%s,%s)"
        values =(sname,fname,mname,phone,address,sclass,ssection)
        cursor.execute(sql,values)
        cursor.execute("COMMIT")
        cursor.execute("SELECT SADMISSION_NO FROM STUDENT WHERE PHONE = %s",(phone,))
        sadmission_no = cursor.fetchall()
        print("|------------------STUDENT PROFILE ADDED SUCCESSFULLY---------------|")
        print("| YOUR ADMISSION_NO : ",sadmission_no)
        cursor.close()
    else:
        print("! ERROR ESTABLISHING MYSQL CONNECTION !")

    input("Press Enter Key To Continue")

#ADDMISSION KEY CHECK FUNCTION

def addmission () :
    cursor = myConnection.cursor()
    if myConnection :
        cursor.execute("SELECT SADMISSION_NO FROM STUDENT")
        data = cursor.fetchall()
        addmission = []
        if data :
            for i in data :
                for j in i :
                    addmission.append(j)
            return tuple(addmission)
        else:
            return 
    else:
        return

#MODULE TO DISPLAY STUDENT'S DATA

def displaystudents():
    cursor = myConnection.cursor()
    try :
        if myConnection:
            classes = ('LKG','UKG','I','II','III','IV','V','VI','VII','VIII','IX','X','XI','XII')
            sec = ('A','B','C')
            for cls in classes :
                print("")
                print("|----------------------------------CLASS = ",cls,'------------------------------------|')
                print("")
                for section in sec :
                    print("SECTION = ",section,)
                    cursor.execute("SELECT * FROM STUDENT WHERE SCLASS = %s AND SSECTION = %s",(cls,section))
                    print(tabulate(cursor,headers = ["STUDENT","FATHER","MOTHER","PHONE","ADDRESS","CLASS","SSECTION","ADMISSION_NO"],tablefmt = 'pretty'))
                    cursor.execute("""COMMIT""")
        else:
            print("! ERROR ESTABLISHING MYSQL CONNECTION !")
    except:
        print("!! NO DATA FOUND !!")

    input(" Press Enter Key To continue ")
    cursor.close()

#MODULE TO DISPLAY ONE STUDENT DATA

def displaystudent():
    cursor=myConnection.cursor()
    if myConnection:
        while True :
            admission_no=input("Enter Addmission_no : ")
            if (admission_no.strip()).isdigit():
                admission_no = int(admission_no)
                if admission_no in addmission():
                    break
                else:
                    print("!!! INVALID INPUT !!!")
            else:
                print("!!! INVALID INPUT !!!")
        
        sql="SELECT * FROM STUDENT WHERE SADMISSION_NO= %s"
        cursor.execute(sql,(admission_no,))
        print(tabulate(cursor,headers = ["STUDENT","FATHER","MOTHER","PHONE","ADDRESS","CLASS","SSECTION","ADMISSION_NO"],tablefmt = 'pretty'))
        cursor.execute("""COMMIT""")
        cursor.close()
    else:
        print("! SOMTHING WENT WRONG,PLEASE TRY AGIAN !")
    
    input(" Press Enter Key To continue ")

#MODULE TO UPDATE STUDENT'S RECORD

def updatestudent():
    cursor=myConnection.cursor()
    if myConnection:
        while True :
            admission_no = input(" Enter Addmission_no : ")
            if (admission_no.strip()).isdigit() :
                admission_no = int(admission_no)
                if admission_no in addmission() :
                    break
                else:
                    print("!!! INVALID INPUT !!!")
            else:
                print("!!! INVALID INPUT !!!")

        sql="SELECT * FROM STUDENT WHERE SADMISSION_NO = %s"
        cursor.execute(sql,(admission_no,))
        data=cursor.fetchall()
        if data:
            fields = ("STUDENT","FATHER","MOTHER","PHONE","ADDRESS","CLASS","SSECTION")
            print("---------------------------------")
            for table in range(len(fields)) :
                print("|PRESS ",table,"TO UPDATE ",fields[table],"\t|")
            print("---------------------------------")
            while True :
                choic=input("Enter Your Choice : ")
                if choic.isdigit():
                    choice=int(choic)
                    break
                else:
                    print("!!! INVALID INPUT !!!")

            if choice == 0:
                while True :
                    name=input("| Enter Name of Student : ").title()
                    if (name.replace(" ","")).isalpha() and len(name) <= 30:
                        break
                    else:
                        print("!!! INVALID INPUT !!!")
                sql="UPDATE STUDENT SET SNAME = %s WHERE SADMISSION_NO =%s"
                cursor.execute(sql,(name,admission_no))
                cursor.execute("COMMIT")
                print("NAME UPDATED")

            elif choice == 1 :
                while True :
                    fname = input("| Enter Father's Name : ").title()
                    if (fname.replace(" ","")).isalpha() and len(fname) <= 30:
                        break 
                sql="UPDATE STUDENT SET FNAME = %s WHERE SADMISSION_NO =%s"
                cursor.execute(sql,(fname,admission_no))
                cursor.execute("COMMIT")
                print("FATHER'S NAME UPDATED")

            elif choice == 2:
                while True :
                    mname = input("| Enter Mother's Name : ").title()
                    if (mname.replace(' ','')).isalpha() and len(mname) <= 30:
                        break 
                sql="UPDATE STUDENT SET MNAME = %s WHERE SADMISSION_NO =%s"
                cursor.execute(sql,(mname,admission_no))
                cursor.execute("COMMIT")
                print("MOTHER'S NAME UPDATED")

            elif choice == 3:
                while True :
                    phone = input("| Enter Contact_no : " )
                    if phone.isdigit() and len(phone) == 10 :
                        break
                sql="UPDATE STUDENT SET PHONE = %s WHERE SADMISSION_NO =%s"
                cursor.execute(sql,(phone,admission_no))
                cursor.execute("COMMIT")
                print("PHONE_NO UPDATED")

            elif choice == 4 :
                while True :
                    address = input("| Enter Address : " )
                    if len(address.strip()) <= 100 :
                        break
                sql="UPDATE STUDENT SET ADDRESS = %s WHERE SADMISSION_NO =%s"
                cursor.execute(sql,(address,admission_no))
                cursor.execute("COMMIT")
                print("ADDRESS UPDATED")

            elif choice == 5 :
                cls_name = {'@':'LKG','0':'UKG','1':'I','2':'II','3':'III','4':'IV','5':'V','6':'VI','7':'VII','8':'VIII','9':'IX','10':'X','11':'XI','12':'XII'}
                print(' -------------------------------')
                for x,y in cls_name.items():
                    print('| PRESS ',x,' FOR ',y,' CLASS \t|')
                print(' -------------------------------')
                while True :
                    s_class = input("| Enter Class : " )
                    if s_class in cls_name.keys():
                        sclass = cls_name[s_class]
                        break 
                sql="UPDATE STUDENT SET SCLASS = %s WHERE SADMISSION_NO =%s"
                cursor.execute(sql,(sclass,admission_no))
                cursor.execute("COMMIT")
                print("CLASS UPDATED")

            elif choice == 6 :
                sec = ('A','B','C')
                print('-----')
                for i in sec :
                    print('|',i,'|')
                print('-----')
                while True :
                    ssection = input("| Enter Section : ").title()
                    if ssection in sec :
                        break
                sql="UPDATE STUDENT SET SSECTION = %s WHERE SADMISSION_NO =%s"
                cursor.execute(sql,(ssection,admission_no))
                cursor.execute("COMMIT")
                print("SECTION UPDATED")

            else:
                print("! Record Not Found Try Again !")
                cursor.close()
        else:
            print("|! NO DATA !|")
    else:
        print("! Somthing Went Wrong ,Please Try Again !")

    input("Press Enter key to continue")

#MODULE TO ISSUE TRANSFER CERTIFICATE

def deletestudent():
    cursor=myConnection.cursor()
    if myConnection:
        while True :
            admission_no=input("ENTER ADMISSION NO OF THE STUDENT :")
            if (admission_no.strip()).isdigit() :
                admission_no = int(admission_no)
                if admission_no in addmission():
                    break
                else:
                    print("!!! INVALID INPUT !!!")
            else:
                print("!!! INVALID INPUT !!!")
        cursor=myConnection.cursor()
        try:
            sql="SELECT * FROM STUDENT WHERE SADMISSION_NO= %s"
            cursor.execute(sql,(admission_no,))
            data=cursor.fetchall()
            if data:
                sql=("DELETE FROM STUDENT WHERE SADMISSION_NO=%s")
                cursor.execute(sql,(admission_no,))
                cursor.execute("COMMIT")
                print("!!! Student's Data Deleted Successfully !!!")
            else:
                print("! Record Not Found , Please Try Again !")
                cursor.close()
        except :
            print("! Record Not Found , Please Try Again !")
    else:
        print("! Somthing Went Wrong ,Please Try Again !")
    
    input(" Press Enter Key To Continue ")

#MODULE TO ENTER MARKS OF THE STUDENT

def marksstudent () :
    if myConnection:
        cursor=myConnection.cursor()
        createTable ="""CREATE TABLE IF NOT EXISTS MARKS(SADMISSION_NO VARCHAR(10) PRIMARY KEY,HINDI INT,ENGLISH INT ,MATH INT ,SCIENCE INT,SOCIAL INT,COMPUTER INT,TOTAL INT ,AVERAGE DECIMAL)"""
        cursor.execute(createTable)
        while True :
            admission_no=input("| Enter Addmission_no of Student : ")
            if (admission_no.strip()).isdigit() :
                admission_no = int(admission_no)
                if admission_no in addmission():
                    break
                else:
                    print("!!! INVALID INPUT !!!")
            else:
                print("!!! INVALID INPUT !!!")
        
        while True :
            hindi = input("| Enter Marks of Hindi : ")
            if hindi.isdigit() and len(hindi) < 3 :
                A = int(hindi)
                break
            else:
                print("!!! INVALID INPUT !!!")
        while True :
            english = input("| Enter Marks of English : ")
            if english.isdigit() and len(english) < 3:
                B = int(english)
                break
            else:
                print("!!! INVALID INPUT !!!")
        while True :
            math = input("| Enter Marks of Maths : ")
            if math.isdigit() and len(math) < 3 :
                C = int(math)
                break
            else:
                print("!!! INVALID INPUT !!!")
        while True :
            science = input("| Enter Marks of Science : ")
            if science.isdigit() and len(science) < 3:
                D = int(science)
                break
            else:
                print("!!! INVALID INPUT !!!")
        while True :
            social = input("| Enter Marks of Social : ")
            if social.isdigit() and len(social) < 3:
                E = int(social)
                break
            else:
                print("!!! INVALID INPUT !!!")
        while True :
            computer =input("| Enter Marks of Computer : ")
            if computer.isdigit() and len(computer) < 3 :
                F = int(computer)
                break
            else:
                print("!!! INVALID INPUT !!!")
                                

        total = A + B + C + D + E + F
        average = total/6

        sql="INSERT INTO MARKS(SADMISSION_NO,HINDI,ENGLISH,MATH,SCIENCE,SOCIAL,COMPUTER,TOTAL,AVERAGE) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        values=(admission_no,A,B,C,D,E,F,total,average)
        cursor.execute(sql,values)
        cursor.execute("COMMIT")
        cursor.close()

        print("|---------------------Marks of the Student Entered Successfully----------------------|")
    else:
        print("! ERROR ESTABLISHING MYSQL CONNECTION !")
    
    input(" Press Enter Key To continue ")

#MODULE TO GENERATE REPORT CARD OF ALL STUDENTS 

def reportcardallstudent ():
    cursor=myConnection.cursor()
    try :
        if myConnection:
            cursor.execute("SELECT * FROM MARKS ")
            print(tabulate(cursor,headers = ["ADMISSION_NO","HINDI","ENGLISH","MATH","SCIENCE","SOCIAL","COMPUTER","TOTAL","AVERAGE"],tablefmt = 'fancy_grid'))
            cursor.execute("""COMMIT""")
            cursor.close()
        else:
            print("! Somthing Went Wrong ,Please Try Again !")
    except :
        print("! No Data Found ,Please Try Again !")

    input(" Press Enter Key To continue ")

#MODULE TO GENERATE REPORT CARD OF ONE STUDENTS

def reportcardonestudent():
    cursor=myConnection.cursor()
    if myConnection:
        while True :
            admission_no=input("Enter Addmission_no of Student :")
            if (admission_no.strip()).isdigit() :
                admission_no = int(admission_no)
                if admission_no in addmission() :
                    break
                else:
                    print("!!! INVALID INPUT !!!")
            else:
                print("!!! INVALID INPUT !!!")
        cursor=myConnection.cursor()
        try :
            sql="SELECT * FROM MARKS WHERE SADMISSION_NO= %s"
            cursor.execute(sql,(admission_no,))
            print(tabulate(cursor,headers = ["ADMISSION_NO","HINDI","ENGLISH","MATH","SCIENCE","SOCIAL","COMPUTER","TOTAL","AVERAGE"],tablefmt = "fancy_grid"))
            cursor.execute("""COMMIT""")
            cursor.close()
        except :
            print("! No Data Found , Please Try Again !")
    else:
        print("! Somthing Went Wrong ,Please Try Again !")
    
    input(" Press Enter Key To continue ")

#MODULE TO ENTER FEES OF THE STUDENTS

def feestudent () :
    if myConnection:
        cursor=myConnection.cursor()
        createTable ="""CREATE TABLE IF NOT EXISTS FEES(SADMISSION_NO VARCHAR(10) PRIMARY KEY , MONTH INT ,TUTION_FEES INT,VVN INT,COMPUTER_FEES INT ,MUSIC_FEES INT, TOTAL INT)"""
        cursor.execute(createTable)
        while True :
            admission_no=input("| Enter Student Addmission n_o :")
            if (admission_no.strip()).isdigit() :
                admission_no = int(admission_no)
                if admission_no in addmission() :
                    break 
                else:
                    print("!!! INVALID INPUT !!!")
            else:
                print("!!! INVALID INPUT !!!")
        while True :
            month=input("| Enter Month In Numric Form (1-12) : ")
            if month.isdigit() and len(month) <=2 :
                month = int(month)
                break
            else:
                print("!!! INVALID INPUT !!!")
        while True :
            tutionfee=input("| Enter Tution Fee : ")
            if tutionfee.isdigit() :
                tutionfee = int(tutionfee)
                break 
            else:
                print("!!! INVALID INPUT !!!")
        while True :
            vvn=input("| EnteR VVN : ")
            if vvn.isdigit() :
                vvn = int(vvn)
                break 
            else:
                print("!!! INVALID INPUT !!!")
        while True :
            computerfee=input("| Enter Computer Fee : ")
            if computerfee.isdigit() :
                computerfee = int(computerfee)
                break 
            else:
                print("!!! INVALID INPUT !!!")
        while True :
            musicfee=input("| Enter Music Fee : ")
            if musicfee.isdigit() :
                musicfee = int(musicfee)
                break
            else:
                print("!!! INVALID INPUT !!!")
                                    

        total = tutionfee + vvn + computerfee + musicfee
        sql="INSERT INTO FEES(SADMISSION_NO,MONTH,TUTION_FEES,VVN,COMPUTER_FEES,MUSIC_FEES,TOTAL) VALUES(%s,%s,%s,%s,%s,%s,%s)"
        values=(admission_no,month,tutionfee,vvn,computerfee,musicfee,total)
        cursor.execute(sql,values)
        cursor.execute("COMMIT")
        cursor.close()
        print("! Fees of Student Accepted Successfully !")
    else:
        print("! ERROR ESTABLISHING MYSQL CONNECTION !") 

    input(" Press Enter Key To continue ")

#MODULE TO GENERATE FEES RECEIPT OF ALL STUDENTS

def feereceiptallstudent():
    cursor=myConnection.cursor()
    try :
        if myConnection:
            cursor.execute("SELECT * FROM FEES")
            print(tabulate(cursor,headers = ["ADMISSION_NO","MONTH","TUTION_FEES","VVN","COMPUTER_FEES","MUSIC_FEES","TOTAL"],tablefmt = 'pipe'))
            cursor.execute("""COMMIT""")
            cursor.close()
        else:
            print("! Somthing Went Wrong ,Please Try Again !")
    except:
        print("! No Data Found , Please Try Again !")

    input(" Press Enter Key To continue ")

#MODULE TO GENERATE FEES RECEIPT OF ONE STUDENT

def feereceiptonestudent():
    cursor=myConnection.cursor()
    if myConnection:
        while True :
            admission_no=input("Enter Addmission n_o of Student : ")
            if (admission_no.strip()).isdigit() :
                admission_no = int(admission_no)
                if admission_no in addmission() :
                    break
                else:
                    print("!!! INVALID INPUT !!!")
            else:
                print("!!! INVALID INPUT !!!")

        cursor=myConnection.cursor()
        sql="SELECT * FROM FEES WHERE SADMISSION_NO= %s"
        cursor.execute(sql,(admission_no,))
        print(tabulate(cursor,headers = ["ADMISSION_NO","MONTH","TUTION_FEES","VVN","COMPUTER_FEES","MUSIC_FEES","TOTAL"],tablefmt = 'pipe'))
        cursor.execute("""COMMIT""")
        cursor.close()
    else:
        print("! Somthing Went Wrong ,Please Try Again !")
    
    input("Press Enter Key To Continue")

#MODULE TO PROVIDE HELP FOR USER

def helpme():
    print("Please, Visit The Offcial Website Of Vidyalaya To Download The Mannual !!!")
    input(" Press Enter Key To continue ")

#MAIN SCREEN SYSTEM

def maindisplay() :
    print(""" __________________________________________________________________________
|                           SESSION 2022-23                                |
|--------------------------------------------------------------------------|
|                               WELCOME                                    |
|                       STUDENT MANAGMENT SYSTEM                           |
|                 DESIGNED AND MAINTAINED BY:TARUN MAWRI                   |
|--------------------------------------------------------------------------|
|                      STUDENT MANAGMENT SYSTEM                            |
|--------------------------------------------------------------------------|
|__________________________________________________________________________|""") 
    myConnection = MYSQLconnectionCheck ()
    if myConnection:
        MYSQLconnection()
        # STARTING POINT OF A SYSTEM
        while True:
            print(""" __________________________________________________________________________
|                                                                          |
| Enter 1 - New Admission.                                                 |
| Enter 2 - Display Student's Data.                                        |
| Enter 3 - Display All Student's Data.                                    |
| Enter 4 - Update Students's Data .                                       |
| Enter 5 - delete Students's Data .                                       |
| Enter 6 - Add Student's Marks Detail.                                    |
| Enter 7 - Generate All Student's Report Card.                            |
| Enter 8 - Generate Student Wise Report Card.                             |
| Enter 9 - Create Student's Fee Receipt.                                  |
| Enter 10 - Generate Student Wise Fees Receipt.                           |
| Enter 11 - Generate Student's Fee Receipt.                               |
| Enter 12- Exit.                                                          | 
|--------------------------------------------------------------------------|
| Enter 0(ZERO) - Help.                                                    |
|--------------------------------------------------------------------------|""")
            choice=input("Please Enter Your Choice : ")
            if choice=='1':
                newstudent()
            elif choice=='2':
                displaystudent()
            elif choice=='3':
                displaystudents()
            elif choice=='4':
                updatestudent()
            elif choice=='5':
                deletestudent()
            elif choice=='6':
                marksstudent()
            elif choice=='7':
                reportcardallstudent()
            elif choice=='8':
                reportcardonestudent()
            elif choice=='9':
                feestudent()
            elif choice=='10':
                feereceiptallstudent()
            elif choice=='11':
                feereceiptonestudent()
            elif choice == '12':
                myConnection.close()
                print("---Thanks For Visit---")
                break
            elif choice=='0':
                helpme()
            else:
                print("!!! Sorry ,May Be You Are Giving Me Wrong Input, Please Try Again !!! ")
    else:
        print("!!! Check Your MYSQL Connection First !!! ")

maindisplay()

# END OF THE PROJECT