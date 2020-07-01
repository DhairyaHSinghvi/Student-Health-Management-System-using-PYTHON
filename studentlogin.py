from tkinter import *
import mysql.connector
from validation import *
from PIL import ImageTk,Image
import os
import datetime
from tkinter import ttk

class app:
    def closeall(self):
        self.welcomeframe.grid_forget()
        self.loginframe.grid_forget()
        self.displaydetailsframe.grid_forget()
        self.specificstudentframe.grid_forget()
        self.foodintakeframe.grid_forget()
        self.caloriesheetframe.grid_forget()
        self.viewmoreframe.grid_forget()
        self.incorrectloginframe.grid_forget()

    def viewmore(self):
        self.closeall()
        self.detailcols=("sfooditem","scategory","stotalcalorie")
        self.detailtree = ttk.Treeview(self.viewmoreframe,column=self.detailcols,show="headings")

        try:
            currentitem=self.tree.focus()
            fid=self.tree.item(currentitem)['values'][0]
            intake="Detailed intake for Date : "+str(fid)
            Label(self.viewmoreframe,text=intake,bg="#D0F0C0",font=('bold',14)).grid(row=1,column=0,padx=10,pady=10)
        

            for x in self.detailcols:
                self.detailtree.heading(x,text=x)
            self.detailtree.grid(row=2,column=0,padx=10,pady=10)
            displaysql="select sfooditem,scategory,stotalcalorie from studentcaloriedatabase where sid=%d and date(stime)='%s'"%(self.studid,fid)
            cur.execute(displaysql)
            result=cur.fetchall()
            for res in result:
                self.detailtree.insert("",END,values=[res['sfooditem'],res['scategory'],res['stotalcalorie']])

            value=0

            for res in result:
                value=value+int(res['stotalcalorie'])

            totalcalvalue="The Total Calorie Intake is "+str(value)
            Label(self.viewmoreframe,text=totalcalvalue,bg="#D0F0C0",font=('bold')).grid(row=3,column=0,columnspan="2",padx=10,pady=10)

            if value<(self.expectedcal-50):
                Label(self.viewmoreframe,text="Your Intake is Low",fg="red",bg="#D0F0C0",font=('bold',16)).grid(row=4,column=0,columnspan="2",padx=10,pady=10)
            elif (value>=(self.expectedcal-50) and value<self.expectedcal+50):
                Label(self.viewmoreframe,text="Your Intake is Adequate",fg="green",bg="#D0F0C0",font=('bold',16)).grid(row=4,column=0,columnspan="2",padx=10,pady=10)
            else:
                Label(self.viewmoreframe,text="Your Intake is High",fg="red",bg="#D0F0C0",font=('bold',16)).grid(row=4,column=0,columnspan="2",padx=10,pady=10)

            Button(self.viewmoreframe,text="Back to Calorie Sheet",command=self.caloriesheet).grid(row=5,column=0,columnspan="2",padx=10,pady=10)

        except IndexError:
            Label(self.caloriesheetframe,text="Please select a day",fg="red",bg="#D0F0C0",font=('bold',16)).grid(row=6,column=0,columnspan="2",padx=10,pady=10)
        
        self.viewmoreframe.grid(row=0,column=0)

    def caloriesheet(self):
        self.closeall()
        Label(self.caloriesheetframe,text="CALORIE SHEET",bg="#D0F0C0").grid(row=0,column=0,columnspan="2",padx=10,pady=10)
        self.detailcols=("sfooditem","scategory","stotalcalorie")
        self.detailtree = ttk.Treeview(self.caloriesheetframe,column=self.detailcols,show="headings")

        self.cols=("stime","stotalcalorie")
        self.tree=ttk.Treeview(self.caloriesheetframe,column=self.cols,show="headings")
        for x in self.cols:
            self.tree.heading(x,text=x)
        self.tree.grid(row=1,column=0,padx=10)
        displaysql="select sum(stotalcalorie) as c,date(stime) as t from studentcaloriedatabase where sid=%d group by date(stime)"%(self.studid)
        cur.execute(displaysql)
        result=cur.fetchall()
        for res in result:
            self.tree.insert("",END,values=[res['t'],res['c']])

        Button(self.caloriesheetframe,text="View More",command=self.viewmore).grid(row=2,column=0,columnspan="2",padx=10,pady=10)
        
        '''
        for x in self.detailcols:
            self.detailtree.heading(x,text=x)
        self.detailtree.grid(row=1,column=0,padx=10)
        displaysql="select sfooditem,scategory,stotalcalorie from studentcaloriedatabase where sid=%d"%(self.studid)
        cur.execute(displaysql)
        result=cur.fetchall()
        for res in result:
            self.detailtree.insert("",END,values=[res['sfooditem'],res['scategory'],res['stotalcalorie']])

        value=0

        for res in result:
            value=value+int(res['stotalcalorie'])

        totalcalvalue="The Total Calorie Intake is "+str(value)
        Label(self.caloriesheetframe,text=totalcalvalue).grid(row=2,column=0,columnspan="2",padx=10,pady=10)

        if value<self.expectedcal:
            Label(self.caloriesheetframe,text="Your Intake is Low",fg="red").grid(row=3,column=0,columnspan="2",padx=10,pady=10)
        elif value==self.expectedcal:
            Label(self.caloriesheetframe,text="Your Intake is Adequate",fg="green").grid(row=3,column=0,columnspan="2",padx=10,pady=10)
        else:
            Label(self.caloriesheetframe,text="Your Intake is High",fg="red").grid(row=3,column=0,columnspan="2",padx=10,pady=10)

        '''
        self.logoutbutton=Button(self.caloriesheetframe,text="Logout",command=self.login)
        self.logoutbutton.grid(row=5,column=0,padx=10,pady=10)
    
        self.caloriesheetframe.grid(row=0,column=0)

    def addtocal(self):
        fooditem=self.valfood.get()
        quantity=self.entryquantity.get()

        getcalsql="select calorie,category from caloriefooditems where name='%s'"%(fooditem)
        cur.execute(getcalsql)
        res=cur.fetchone()

        cal=res['calorie']
        cat=res['category']
        finalcal=int(quantity)*int(cal)
    
        putsql="insert into studentcaloriedatabase(sid,srollno,sfooditem,scategory,stotalcalorie) values(%d,%d,'%s','%s',%d)"%(self.studid,self.rollno,fooditem,cat,finalcal)
        cur.execute(putsql)
        con.commit()
        print("added")     

    def foodintake(self):
        self.closeall()
        labeladd=Label(self.foodintakeframe,text="Enter the food items you have consumed in a day - ",bg="#D0F0C0")
        labeladd.grid(row=0,column=0,columnspan="2",padx=10,pady=10)

        foodnamesql="select name from caloriefooditems"
        cur.execute(foodnamesql)
        result=cur.fetchall()
        foodname=[]
        for x in result:
            foodname.append(x['name'])

        self.valfood=StringVar()
        self.valfood.set("----Select Food Item---")
        
        self.labelfooddd=Label(self.foodintakeframe,text="Food Item : ",bg="#D0F0C0")
        self.labelfooddd.grid(row=2,column=0,padx=5,pady=5)
        self.dropdownfood=OptionMenu(self.foodintakeframe,self.valfood,*foodname)
        self.dropdownfood.grid(row=2,column=1,padx=5,pady=5)

        labelquantity=Label(self.foodintakeframe,text="Quantity (1 represents 100gm) : ",bg="#D0F0C0")
        labelquantity.grid(row=3,column=0,padx=5,pady=5)
        self.entryquantity=Entry(self.foodintakeframe)
        self.entryquantity.grid(row=3,column=1,padx=5,pady=5)

        self.buttonaddtofoodlist=Button(self.foodintakeframe,text="Add to Calorie List",command=self.addtocal)
        self.buttonaddtofoodlist.grid(row=4,column=0,padx=5,pady=5)

        self.logoutbutton=Button(self.foodintakeframe,text="Logout",command=self.login)
        self.logoutbutton.grid(row=5,column=0,padx=10,pady=10)

        self.foodintakeframe.grid(row=0,column=0)

    def displaydetails(self):
        self.closeall()
        self.getid=int(self.entryid.get())
       
        getvaluesql="select * from studentdetails where srollno=%d"%(self.getid)
        cur.execute(getvaluesql)
        res=cur.fetchone()
        self.studid=res['sid']
        name=res['sname']
        age=res['sage']
        classs=res['sclass']
        self.rollno=res['srollno']
        gender=res['sgender']
        types=res['stype']
        height=res['sheight']
        weight=res['sweight']
        bmi=res['sbmi']

        if types=="Moderately Active":
            types="Moderately_Active"

        getcalorievaluesql="select %s from calorieneed where age=%d and gender='%s'"%(types,age,gender)
        cur.execute(getcalorievaluesql)
        calres=cur.fetchone()
        self.expectedcal=calres[types]

        stringhello="Hello "+name.upper()
        stringclass="Class : "+str(classs)
        stringage="Age : "+str(age)
        stringrollno="Roll Number : "+str(self.rollno)
        stringgender="Gender : "+gender
        stringtype="Physical Activity Level : "+types
        stringheight="Height : "+str(height)
        stringweight="Weight : "+str(weight)
        stringbmi="Body Mass Index : "+str(bmi)
        stringexpcal="Expected Calorie Intake per day is "+str(self.expectedcal)

        labelhello=Label(self.displaydetailsframe,text=stringhello,bg="#D0F0C0")
        labelhello.grid(row=0,column=0,padx=10,pady=20)

        labeld1=Label(self.displaydetailsframe,text=stringclass,bg="#D0F0C0")
        labeld1.grid(row=1,column=0,padx=10,pady=10)
        labeld2=Label(self.displaydetailsframe,text=stringrollno,bg="#D0F0C0")
        labeld2.grid(row=1,column=1,padx=10,pady=10)
        labeld3=Label(self.displaydetailsframe,text=stringage,bg="#D0F0C0")
        labeld3.grid(row=1,column=2,padx=10,pady=10)

        labeld4=Label(self.displaydetailsframe,text=stringheight,bg="#D0F0C0")
        labeld4.grid(row=2,column=0,padx=10,pady=10)
        labeld5=Label(self.displaydetailsframe,text=stringweight,bg="#D0F0C0")
        labeld5.grid(row=2,column=1,padx=10,pady=10)
        labeld6=Label(self.displaydetailsframe,text=stringbmi,bg="#D0F0C0")
        labeld6.grid(row=2,column=2,padx=10,pady=10)

        labeld7=Label(self.displaydetailsframe,text=stringgender,bg="#D0F0C0")
        labeld7.grid(row=3,column=0,padx=10,pady=10)
        labeld8=Label(self.displaydetailsframe,text=stringtype,bg="#D0F0C0")
        labeld8.grid(row=3,column=1,padx=10,pady=10)
        labeld9=Label(self.displaydetailsframe,text=stringexpcal,bg="#D0F0C0")
        labeld9.grid(row=3,column=2,padx=10,pady=10)

        '''
        try:
            getvaluesql="select * from studentdetails where srollno=%d"%(self.getid)
            cur.execute(getvaluesql)
            result=cur.fetchone()
            self.studid=result['sid']
            name=result['sname']
            age=result['sage']
            classs=result['sclass']
            self.rollno=result['srollno']
            gender=result['sgender']
            types=result['stype']
            height=result['sheight']
            weight=result['sweight']
            bmi=result['sbmi']

            if types=="Moderately Active":
                types="Moderately_Active"

            getcalorievaluesql="select %s from calorielist where age=%d and gender='%s'"%(types,age,gender)
            cur.execute(getcalorievaluesql)
            calres=cur.fetchone()
            self.expectedcal=calres[types]

            stringhello="Hello "+name.upper()
            stringclass="Class : "+str(classs)
            stringage="Age : "+str(age)
            stringrollno="Roll Number : "+str(self.rollno)
            stringgender="Gender : "+gender
            stringtype="Physical Activity Level : "+types
            stringheight="Height : "+str(height)
            stringweight="Weight : "+str(weight)
            stringbmi="Body Mass Index : "+str(bmi)
            stringexpcal="Your Expected Calorie Intake per day is "+self.expectedcal

            labelhello=Label(self.displaydetailsframe,text=stringhello)
            labelhello.grid(row=0,column=0,padx=10,pady=20)

            labeld1=Label(self.displaydetailsframe,text=stringclass)
            labeld1.grid(row=1,column=0,padx=10,pady=10)
            labeld2=Label(self.displaydetailsframe,text=stringrollno)
            labeld2.grid(row=1,column=1,padx=10,pady=10)
            labeld3=Label(self.displaydetailsframe,text=stringage)
            labeld3.grid(row=1,column=2,padx=10,pady=10)

            labeld4=Label(self.displaydetailsframe,text=stringheight)
            labeld4.grid(row=2,column=0,padx=10,pady=10)
            labeld5=Label(self.displaydetailsframe,text=stringweight)
            labeld5.grid(row=2,column=1,padx=10,pady=10)
            labeld6=Label(self.displaydetailsframe,text=stringbmi)
            labeld6.grid(row=2,column=2,padx=10,pady=10)

            labeld7=Label(self.displaydetailsframe,text=stringgender)
            labeld7.grid(row=3,column=0,padx=10,pady=10)
            labeld8=Label(self.displaydetailsframe,text=stringtype)
            labeld8.grid(row=3,column=1,padx=10,pady=10)
            labeld9=Label(self.displaydetailsframe,text=stringexpcal)
            labeld9.grid(row=3,column=2,padx=10,pady=10)
        except TypeError:
            labelexcept=Label(self.displaydetailsframe,text="No such student is added to the database",fg="red")
            labelexcept.grid(row=4,column=0,padx=10,pady=10)'''

        self.logoutbutton=Button(self.displaydetailsframe,text="Logout",command=self.login)
        self.logoutbutton.grid(row=5,column=0,padx=10,pady=10)

        self.displaydetailsframe.grid(row=0,column=0)

    def mainpage(self):
        self.closeall()
        if (self.entryid.get()==self.entrypass.get()):
            mainmenu=Menu(self.tk)
            mainmenu.add_command(label="Profile",command=self.displaydetails)
            mainmenu.add_command(label="Food Intake",command=self.foodintake)
            mainmenu.add_command(label="Calorie Sheet",command=self.caloriesheet)
            self.displaydetails()

            self.tk.configure(menu=mainmenu)
        else:
            Label(self.incorrectloginframe,text="Enter correct Credentials",bg="#D0F0C0").grid(row=0,column=0,padx=10,pady=10)
            self.loginbutton=Button(self.incorrectloginframe,text="Login",command=self.login)
            self.loginbutton.grid(row=1,column=0,padx=10,pady=10)

            self.incorrectloginframe.grid(row=0,column=0)

        

    def login(self):
        self.closeall()
        labelenter=Label(self.loginframe,text="Enter your credentials - ",bg="#D0F0C0")
        labelenter.grid(row=0,column=0,columnspan="2",padx=10,pady=10)

        labelenterid=Label(self.loginframe,text="Enter your RollNo : ",bg="#D0F0C0")
        labelenterid.grid(row=1,column=0,padx=10,pady=10)
        self.entryid=Entry(self.loginframe)
        self.entryid.grid(row=1,column=1,padx=10,pady=10)

        labelenterpass=Label(self.loginframe,text="Enter Password : ",bg="#D0F0C0")
        labelenterpass.grid(row=2,column=0,padx=10,pady=10)
        self.entrypass=Entry(self.loginframe)
        self.entrypass.grid(row=2,column=1,padx=10,pady=10)

        self.buttonlog=Button(self.loginframe,text="Login",command=self.mainpage)
        self.buttonlog.grid(row=3,column=0,columnspan="2",padx=10,pady=10)
        
        self.loginframe.grid(row=0,column=0)

    
    def __init__(self,tk):
        self.tk=tk
        tk.title("Student Health Tracking App")
        self.welcomeframe=Frame(self.tk,bg="#D0F0C0")
        self.loginframe=Frame(self.tk,bg="#D0F0C0")
        self.displaydetailsframe=Frame(self.tk,bg="#D0F0C0")
        self.specificstudentframe=Frame(self.tk,bg="#D0F0C0")
        self.foodintakeframe=Frame(self.tk,bg="#D0F0C0")
        self.caloriesheetframe=Frame(self.tk,bg="#D0F0C0")
        self.viewmoreframe=Frame(self.tk,bg="#D0F0C0")
        self.incorrectloginframe=Frame(self.tk,bg="#D0F0C0")

        self.labelwelcome=Label(self.welcomeframe,text="Welcome to Student Health Tracker",bg="#D0F0C0",font=('Algerian',16))
        self.labelwelcome.grid(row=0,column=0,padx=10,pady=10)

        Button(self.welcomeframe,text="Login",command=self.login).grid(row=1,column=0,padx=10,pady=10)

        self.welcomeframe.grid(row=0,column=0)
        #self.tk.configure(menu=adminmenu)
        



#mainprogram
con=mysql.connector.connect(host="localhost",user="root",passwd="",database="projectapp")
cur=con.cursor(dictionary=True,buffered=True)
tk=Tk()
obj=app(tk)
tk.mainloop()
