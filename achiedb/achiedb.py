#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as lite
import urllib.request
from parser import HTMLTableParser
from tabulate import tabulate
import sys

if sys.argv[1]=="update":
   
    with urllib.request.urlopen("http://tibia.wikia.com/wiki/Achievements/DPL") as sock:
        htmlSource = sock.read()
    
    xhtml = htmlSource.decode('utf-8')
    p = HTMLTableParser()
    p.feed(xhtml)
    
    achietab = p.tables[0][1:]
    
    achiedata = []
    it = 0
    for achie in achietab:
        achiedata.append([it] + achie[0:3])
        it+=1
    
    con = lite.connect('achie.db')
    
    with con:
        
        cur = con.cursor()    
        
        cur.execute("DROP TABLE IF EXISTS Achievements_Data")
        cur.execute("CREATE TABLE Achievements_Data(Id INT, Name TEXT, Grade INT, Points INT)")
        cur.executemany("INSERT INTO Achievements_Data VALUES(?, ?, ?, ?)", achiedata)
        print("List of achievements updated.")

if sys.argv[1]=="create":
    if len(sys.argv)==3:
        con = lite.connect('achie.db')
        with con:
            cur = con.cursor()
            cur.execute("CREATE TABLE Achievements_"+sys.argv[2]+"(Id INT, Name TEXT, Grade INT, Points INT)")
            print("New table for character "+sys.argv[2]+" created.")
    else:
        print("create requires exactly one argument: the name of the character")

if sys.argv[1]=="complete":
    if len(sys.argv)==4:
        con = lite.connect('achie.db')
        with con:
            cur = con.cursor()
            print("INSERT INTO Achievements_"+sys.argv[2]+" SELECT * FROM Achievements_Data WHERE Name LIKE '"+sys.argv[3]+"'")
            cur.execute("INSERT INTO Achievements_"+sys.argv[2]+" SELECT * FROM Achievements_Data WHERE Name LIKE '"+sys.argv[3]+"'")
            print("Achievement '"+sys.argv[3]+"' completed! GZ")
    else:
        print("complete requires exactly two arguments: the name of the character and the achievement which is completed")

if sys.argv[1]=="show":
    if len(sys.argv)==3:
        con = lite.connect('achie.db')
        with con:
            cur = con.cursor()
            cur.execute("SELECT * FROM Achievements_"+sys.argv[2])
            print(tabulate(cur.fetchall()))

    else:
        print("show requires exactly one argument: the name of the character")
 
if sys.argv[1]=="count":
    if len(sys.argv)==3:
        con = lite.connect('achie.db')
        with con:
            cur = con.cursor()
            cur.execute("SELECT * FROM Achievements_"+sys.argv[2])
            achietab=cur.fetchall()
            sum = 0
            for achie in achietab:
                sum += achie[3]
            print(sum)

    else:
        print("show requires exactly one argument: the name of the character")
