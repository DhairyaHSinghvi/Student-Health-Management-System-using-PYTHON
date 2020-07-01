import re
from tkinter import *

def checkname(name):
    if name=="":
        error="Please enter name"
        return error
    elif not (re.match("^[A-Za-z]{3,7}$",name)):
        error="Name must contain only alphabets and minimum 3 and maximum length of 7"
        return error
    else:
        return name


def checkage(nos):
    if nos=="":
        error="Please enter age"
        return error
    elif not (re.match("^[0-9]{1,2}$",nos)):
        error="Please enter only numbers"
        return error
    elif (int(nos)>25 and int(nos)<4):
        error="Age should be between 4yrs and 25 yrs"
        return error
    else:
        return nos

def checkclass(nos):
    if nos=="":
        error="Please enter class"
        return error
    elif not (re.match("^[0-9]{1,2}$",nos)):
        error="Please enter only numbers!!"
        return error
    else:
        return nos

def checkrollno(nos):
    if nos=="":
        error="Please enter rollno"
        return error
    elif not (re.match("^[0-9]{1,}$",nos)):
        error="Please enter only numbers"
        return error
    else:
        return nos

def checkheight(nos):
    if nos=="":
        error="Please enter height"
        return error
    else:
        return nos

def checkweight(nos):
    if nos=="":
        error="Please enter weight"
        return error
    else:
        return nos

def checkbmi(nos):
    if nos=="":
        error="Please calculate bmi"
        return error
    else:
        return nos

        
