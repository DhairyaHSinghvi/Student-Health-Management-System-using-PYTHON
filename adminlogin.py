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
        self.dashboardframe.grid_forget()
        self.addstudentframe.grid_forget()
        self.loginframe.grid_forget()
        self.displaydetailsframe.grid_forget()
        self.specificstudentframe.grid_forget()
        self.foodintakeframe.grid_forget()
        self.caloriesheetframe.grid_forget()
        self.viewmoreframe.grid_forget()
        self.viewallframe.grid_forget()

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
        self.feed=0
        self.count=0
        for res in result:
            self.count=self.count+1
            self.feed=self.feed+res['c']
            self.tree.insert("",END,values=[res['t'],res['c']])

        self.average=self.feed/self.count
        if self.average<(self.expectedcal-50):
            self.feedback="low"
        elif (self.average>=(self.expectedcal-50) and self.average<self.expectedcal+50):
            self. feedback="adequate"
        else:
            self.feedback="high"

        cur.execute("update studentdetails set sfeedback='%s' where sid=%d"%(self.feedback,self.studid))
        con.commit()


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
        mainmenu=Menu(self.tk)
        mainmenu.add_command(label="Profile",command=self.displaydetails)
        mainmenu.add_command(label="Food Intake",command=self.foodintake)
        mainmenu.add_command(label="Calorie Sheet",command=self.caloriesheet)
        mainmenu.add_command(label="Back to Admin Page",command=self.main)
        self.displaydetails()

        self.tk.configure(menu=mainmenu)

    def gotospecificstudent(self):
        self.closeall()
        buttonback=Button(self.specificstudentframe,text="Back",command=self.addstudent)
        buttonback.grid(row=0,column=0,padx=10,pady=10)
        
        labelenterid=Label(self.specificstudentframe,text="Enter the Student's RollNo : ",bg="#EFC0FE")
        labelenterid.grid(row=1,column=0,padx=10,pady=10)
        self.entryid=Entry(self.specificstudentframe)
        self.entryid.grid(row=1,column=1,padx=10,pady=10)

        buttonnext=Button(self.specificstudentframe,text="Continue",command=self.mainpage)
        buttonnext.grid(row=2,column=0,columnspan="2",padx=10,pady=10)
        
        self.specificstudentframe.grid(row=0,column=0)
        

    def login(self):
        self.closeall()
        labelenter=Label(self.loginframe,text="Enter Student's Credentials - ",bg="#EFC0FE")
        labelenter.grid(row=0,column=0,columnspan="2",padx=10,pady=10)

        labelenterid=Label(self.loginframe,text="Enter the Student's RollNo : ",bg="#EFC0FE")
        labelenterid.grid(row=1,column=0,padx=10,pady=10)
        self.entryid=Entry(self.loginframe)
        self.entryid.grid(row=1,column=1,padx=10,pady=10)

        labelenterpass=Label(self.loginframe,text="Enter the Password : ",bg="#EFC0FE")
        labelenterpass.grid(row=2,column=0,padx=10,pady=10)
        self.entrypass=Entry(self.loginframe)
        self.entrypass.grid(row=2,column=1,padx=10,pady=10)

     
        self.buttonlog=Button(self.loginframe,text="View Student",command=self.mainpage)
        self.buttonlog.grid(row=3,column=0,columnspan="2",padx=10,pady=10)

        
        self.loginframe.grid(row=0,column=0)

    def addtodb(self):
        name=self.entrysname.get()
        age=self.entrysage.get()
        sclass=self.entrysclass.get()
        rollno=self.entrysrollno.get()
        gender=self.valgender.get()
        types=self.valtype.get()
        h=self.entrysheight.get()
        w=self.entrysweight.get()
        bmi=self.bmi
        namemsg=checkname(name)
        agemsg=checkage(age)
        classmsg=checkclass(sclass)
        rollnomsg=checkrollno(rollno)
        hmsg=checkheight(h)
        wmsg=checkweight(w)
        bmimsg=checkbmi(bmi)
        if(namemsg==name and agemsg==age and classmsg==sclass and rollnomsg==rollno and hmsg==h and wmsg==w and bmimsg==bmi):
            insertsql="insert into studentdetails(sname,sage,sclass,srollno,sgender,stype,sheight,sweight,sbmi) values ('%s',%d,%d,%d,'%s','%s',%f,%f,%f)"%(name,int(age),int(sclass),int(rollno),gender,types,float(h),float(w),float(bmi))
            cur.execute(insertsql)
            con.commit()
            labelsuccess=Label(self.addstudentframe,text="Student Added Successfully",bg="#EFC0FE")
            labelsuccess.grid(row=11,column=0,columnspan="2",padx=10,pady=10)

            #buttonnext=Button(self.addstudentframe,text="Next",command=self.gotospecificstudent)
            #buttonnext.grid(row=12,column=0,columnspan="2",padx=10,pady=10)

        else:
            if(namemsg!=name):
                Label(self.addstudentframe,text=namemsg,fg="red",bg="#EFC0FE").grid(row=1,column=2,padx=10,pady=10)

            if(agemsg!=age):
                Label(self.addstudentframe,text=agemsg,fg="red",bg="#EFC0FE").grid(row=2,column=2,padx=10,pady=10)
                                                                      
            if(classmsg!=sclass):
                Label(self.addstudentframe,text=classmsg,fg="red",bg="#EFC0FE").grid(row=3,column=2,padx=10,pady=10)
                
            if(rollnomsg!=rollno):
                Label(self.addstudentframe,text=rollnomsg,fg="red",bg="#EFC0FE").grid(row=4,column=2,padx=10,pady=10)

            if(hmsg!=h):
                Label(self.addstudentframe,text=hmsg,fg="red",bg="#EFC0FE").grid(row=7,column=2,padx=10,pady=10)

            if(wmsg!=w):
                Label(self.addstudentframe,text=wmsg,fg="red",bg="#EFC0FE").grid(row=8,column=2,padx=10,pady=10)

            if(bmimsg!=bmi):
                Label(self.addstudentframe,text=bmimsg,fg="red",bg="#EFC0FE").grid(row=9,column=2,padx=10,pady=10)
        

    def calbmi(self):
        self.bmi=float(self.entrysweight.get())/(float(self.entrysheight.get())*float(self.entrysheight.get()))
        labelsbmi=Label(self.addstudentframe,text=round(self.bmi),bg="#EFC0FE")
        labelsbmi.grid(row=9,column=1,padx=10,pady=10)

    def addstudent(self):
        self.closeall()
        labelenterdetails=Label(self.addstudentframe,text="Enter the student's details below",bg="#EFC0FE")
        labelenterdetails.grid(row=0,column=0,columnspan="2",padx=10,pady=10)

        labelsname=Label(self.addstudentframe,text="Name : ",bg="#EFC0FE")
        labelsname.grid(row=1,column=0,padx=10,pady=10)
        self.entrysname=Entry(self.addstudentframe)
        self.entrysname.grid(row=1,column=1,padx=10,pady=10)

        labelsage=Label(self.addstudentframe,text="Age : ",bg="#EFC0FE")
        labelsage.grid(row=2,column=0,padx=10,pady=10)
        self.entrysage=Entry(self.addstudentframe)
        self.entrysage.grid(row=2,column=1,padx=10,pady=10)

        labelsclass=Label(self.addstudentframe,text="Class : ",bg="#EFC0FE")
        labelsclass.grid(row=3,column=0,padx=10,pady=10)
        self.entrysclass=Entry(self.addstudentframe)
        self.entrysclass.grid(row=3,column=1,padx=10,pady=10)

        labelsrollno=Label(self.addstudentframe,text="Roll Number : ",bg="#EFC0FE")
        labelsrollno.grid(row=4,column=0,padx=10,pady=10)
        self.entrysrollno=Entry(self.addstudentframe)
        self.entrysrollno.grid(row=4,column=1,padx=10,pady=10)

        self.valgender=StringVar()
        self.choicegender=("male","female")
        self.valgender.set("---Gender---")
        labelgender=Label(self.addstudentframe,text="Gender : ",bg="#EFC0FE")
        labelgender.grid(row=5,column=0,padx=10,pady=10)
        self.genderdd=OptionMenu(self.addstudentframe,self.valgender,*self.choicegender)
        self.genderdd.grid(row=5,column=1,padx=10,pady=10)

        self.valtype=StringVar()
        self.choicetype=("Sedentary","Moderately Active","Active")
        self.valtype.set("---Type---")
        labeltype=Label(self.addstudentframe,text="Type of Student : ",bg="#EFC0FE")
        labeltype.grid(row=6,column=0,padx=10,pady=10)
        self.typedd=OptionMenu(self.addstudentframe,self.valtype,*self.choicetype)
        self.typedd.grid(row=6,column=1,padx=10,pady=10)

        labelsheight=Label(self.addstudentframe,text="Height (in m) : ",bg="#EFC0FE")
        labelsheight.grid(row=7,column=0,padx=10,pady=10)
        self.entrysheight=Entry(self.addstudentframe)
        self.entrysheight.grid(row=7,column=1,padx=10,pady=10)

        labelsweight=Label(self.addstudentframe,text="Weight (in kg) : ",bg="#EFC0FE")
        labelsweight.grid(row=8,column=0,padx=10,pady=10)
        self.entrysweight=Entry(self.addstudentframe)
        self.entrysweight.grid(row=8,column=1,padx=10,pady=10)

        self.buttonbmi=Button(self.addstudentframe,text="Calculate BMI",command=self.calbmi)
        self.buttonbmi.grid(row=9,column=0,padx=10,pady=10)

        self.buttonaddtodb=Button(self.addstudentframe,text="Add to Database",command=self.addtodb)
        self.buttonaddtodb.grid(row=10,column=0,padx=10,pady=10)

        self.addstudentframe.grid(row=0,column=0)

    def viewall(self):
        self.closeall()
        
        self.viewallcols=("sid","sname","sage","sclass","srollno","sgender","stype")
        self.viewalltree=ttk.Treeview(self.viewallframe,column=self.viewallcols,show="headings")
        for x in self.viewallcols:
            self.viewalltree.heading(x,text=x)
        self.viewalltree.grid(row=1,column=0,padx=10,pady=10)
        displaysql="select * from studentdetails"
        cur.execute(displaysql)
        result=cur.fetchall()
        for res in result:
            self.viewalltree.insert("",END,values=[res['sid'],res['sname'],res['sage'],res['sclass'],res['srollno'],res['sgender'],res['stype']])
        

        self.viewallframe.grid(row=0,column=0)

    def dashboard(self):
        self.closeall()
        self.labelwelcome=Label(self.dashboardframe,text="Welcome to Student Health Tracker",bg="#D0F0C0",font=('Algerian',16))
        self.labelwelcome.grid(row=0,column=0,padx=10,pady=10)

        totalsql="select count(sid) as c from studentdetails"
        cur.execute(totalsql)
        res=cur.fetchall()
        total=[]
        for x in res:
            total.append(x['c'])
        totalstudents="Total Students : "+str(total[0])
        Label(self.dashboardframe,text=totalstudents,font=("Helvetica", 10, "bold"),bg="#EFC0FE").grid(row=1,column=0,padx=10,pady=10)

        totallow="select count(sfeedback) as l from studentdetails where sfeedback='low'"
        cur.execute(totallow)
        res=cur.fetchall()
        total=[]
        for x in res:
            total.append(x['l'])
        totallowstudents="Total Students having LOW Calorie Intake : "+str(total[0])
        Label(self.dashboardframe,text=totallowstudents,font=("Helvetica", 10, "bold"),bg="#EFC0FE").grid(row=2,column=0,padx=10,pady=10)

        totalad="select count(sfeedback) as l from studentdetails where sfeedback='adequate'"
        cur.execute(totalad)
        res=cur.fetchall()
        total=[]
        for x in res:
            total.append(x['l'])
        totaladstudents="Total Students having ADEQUATE Calorie Intake : "+str(total[0])
        Label(self.dashboardframe,text=totaladstudents,font=("Helvetica", 10, "bold"),bg="#EFC0FE").grid(row=3,column=0,padx=10,pady=10)

        totalhigh="select count(sfeedback) as l from studentdetails where sfeedback='high'"
        cur.execute(totalhigh)
        res=cur.fetchall()
        total=[]
        for x in res:
            total.append(x['l'])
        totalhighstudents="Total Students having HIGH Calorie Intake : "+str(total[0])
        Label(self.dashboardframe,text=totalhighstudents,font=("Helvetica", 10, "bold"),bg="#EFC0FE").grid(row=4,column=0,padx=10,pady=10)



        self.dashboardframe.grid(row=0,column=0)

    def main(self):

        adminmenu=Menu(self.tk)
        adminmenu.add_command(label="Dashboard",command=self.dashboard)
        adminmenu.add_command(label="Add Student",command=self.addstudent)
        adminmenu.add_command(label="View Student",command=self.viewall)
        adminmenu.add_command(label="Login",command=self.login)

        '''img = ImageTk.PhotoImage(Image.open("food.png"))
        panel = Label(self.tk, image = img)
        panel.grid(row=0,column=1)'''

        
        self.dashboard()

        self.welcomeframe.grid(row=0,column=0)
        self.tk.configure(menu=adminmenu)

    
    def __init__(self,tk):
        self.tk=tk
        #tk.geometry("700x700")
        tk.title("Student Health Tracking App")
        self.welcomeframe=Frame(self.tk,bg="#EFC0FE")
        self.dashboardframe=Frame(self.tk,bg="#EFC0FE")
        self.addstudentframe=Frame(self.tk,bg="#EFC0FE")
        self.loginframe=Frame(self.tk,bg="#EFC0FE")
        self.displaydetailsframe=Frame(self.tk,bg="#D0F0C0")
        self.specificstudentframe=Frame(self.tk,bg="#EFC0FE")
        self.foodintakeframe=Frame(self.tk,bg="#D0F0C0")
        self.caloriesheetframe=Frame(self.tk,bg="#D0F0C0")
        self.viewmoreframe=Frame(self.tk,bg="#D0F0C0")
        self.viewallframe=Frame(self.tk,bg="#EFC0FE")

        self.main()


        



#mainprogram
con=mysql.connector.connect(host="localhost",user="root",passwd="",database="projectapp")
cur=con.cursor(dictionary=True,buffered=True)
tk=Tk()
obj=app(tk)
tk.mainloop()
