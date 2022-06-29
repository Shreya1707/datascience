import pandas as pd
from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect
from django.contrib import messages
import os
import json
import csv
import MySQLdb 
from twilio.rest import Client
import random
import smtplib
import streamlit as st
import plotly_express as px
import glob#to get csv files from a folder
otpgen=random.randint(100000,999999)
def otpverify(request):
    if request.method=='POST':
        myotp=request.POST['otp']
        if int(myotp)==int(otpgen):
            print("Verified")
            return HttpResponseRedirect('/mydata/')
        else:
            print("Please Check your OTP again")
            messages.add_message(request, messages.INFO, 'Incorrect otp!')
    return render(request,'otp.html')
def home(request):
    if request.method=='POST':
        db=MySQLdb.connect("localhost","root","shreya","up")
        mouse=db.cursor()
        user_verification = request.POST['username']  
        pass_verification = request.POST['password']
        emailid = request.POST['email']
        sql = "select * from userpass where username = %s and password = %s"
        mouse.execute(sql,[(user_verification),(pass_verification)])
        results = mouse.fetchall()
        if results:
            for i in results:
                print("Logged in successfully!")
                otp=str(otpgen)+" is your otp."
                s = smtplib.SMTP('smtp.gmail.com', 587)
                s.starttls()
                s.login("shreyashah17dps@gmail.com", "gevpoufytojzavxz")
                #App password and 2-step verification 
                s.sendmail('&&&&&&&&&&&',emailid,otp) 
                return HttpResponseRedirect('/otp/')
            #Redirect is used to call another function. 
        else:
            messages.add_message(request, messages.INFO, 'Incorrect username or password.')
    return render(request,'login.html')

def upload(request):
    if request.method=='POST':
        db=MySQLdb.connect("localhost","root","shreya","up")
        mouse=db.cursor()
        uploaded_file=request.FILES['document']
        country_name=request.POST['country']
        date_of_report=request.POST['number']
        myfile=FileSystemStorage()
        filename=myfile.save(uploaded_file.name,uploaded_file)#Saving file
        path_of_file=myfile.path(filename)#Path of file
        try:
            if '.json' in uploaded_file.name:
                df=pd.read_json(path_of_file)
                try:
                    #Chk if file already exists
                    df = pd.read_csv('E://CODING//project//csv_files//'+country_name+' '+date_of_report+' '+'Sales.csv')
                except:
                    #If file does not exist
                    sql = "INSERT INTO mydatabase (country, year, version) VALUES (%s, %s, %s)"  
                    val=(country_name,date_of_report,'0')
                    mouse.execute(sql,val)
                    db.commit()
                    df.to_csv('E:\CODING\project\csv_files/'+country_name+' '+date_of_report+' '+"Sales"+".csv",index=False)
                else:
                    #If file exists
                    sql1="select * from mydatabase where country = %s and year = %s"
                    mouse.execute(sql1,[(country_name),(date_of_report)])
                    data=mouse.fetchall()
                    print(len(data)," no of lines")
                    sql2="INSERT INTO mydatabase (country, year, version) VALUES (%s, %s, %s)"
                    val=(country_name,date_of_report,len(data))
                    mouse.execute(sql2,val)
                    version=int(len(data))
                    df.to_csv('E:\CODING\project\csv_files/'+country_name+' '+date_of_report+' '+"Sales"+"_"+str(version)+".csv",index=False)
                    db.commit()
            elif '.csv' in uploaded_file.name:
                df=pd.read_csv(path_of_file)
                try:
                    #Chk if file already exists
                    df = pd.read_csv('E://CODING//project//csv_files//'+country_name+' '+date_of_report+' '+'Sales.csv')
                except:
                    #If file does not exist
                    sql = "INSERT INTO mydatabase (country, year, version) VALUES (%s, %s, %s)"  
                    val=(country_name,date_of_report,'0')
                    mouse.execute(sql,val)
                    db.commit()
                    df.to_csv('E:\CODING\project\csv_files/'+country_name+' '+date_of_report+' '+"Sales"+".csv",index=False)
                else:
                    #If file exists
                    sql1="select * from mydatabase where country = %s and year = %s"
                    mouse.execute(sql1,[(country_name),(date_of_report)])
                    data=mouse.fetchall()
                    print(len(data)," no of lines")
                    sql2="INSERT INTO mydatabase (country, year, version) VALUES (%s, %s, %s)"
                    val=(country_name,date_of_report,len(data))
                    mouse.execute(sql2,val)
                    version=int(len(data))
                    df.to_csv('E:\CODING\project\csv_files/'+country_name+' '+date_of_report+' '+"Sales"+"_"+str(version)+".csv",index=False)
                    db.commit()
            elif '.xls' or '.xlsx' or '.xlsm' or '.xlsb' or '.odf' or '.ods' or '.odt' in uploaded_file.name:#install openpyxsl
                df=pd.read_excel(path_of_file)
                try:
                    #Chk if file already exists
                    df = pd.read_csv('E://CODING//project//csv_files//'+country_name+' '+date_of_report+' '+'Sales.csv')
                except:
                    #If file does not exist
                    sql = "INSERT INTO mydatabase (country, year, version) VALUES (%s, %s, %s)"  
                    val=(country_name,date_of_report,'0')
                    mouse.execute(sql,val)
                    db.commit()
                    df.to_csv('E:\CODING\project\csv_files/'+country_name+' '+date_of_report+' '+"Sales"+".csv",index=False)
                else:
                    #If file exists
                    sql1="select * from mydatabase where country = %s and year = %s"
                    mouse.execute(sql1,[(country_name),(date_of_report)])
                    data=mouse.fetchall()
                    print(len(data)," no of lines")
                    sql2="INSERT INTO mydatabase (country, year, version) VALUES (%s, %s, %s)"
                    val=(country_name,date_of_report,len(data))
                    mouse.execute(sql2,val)
                    version=int(len(data))
                    df.to_csv('E:\CODING\project\csv_files/'+country_name+' '+date_of_report+' '+"Sales"+"_"+str(version)+".csv",index=False)
                    db.commit()
            return HttpResponseRedirect('/thankyou/')
        except:
            messages.add_message(request, messages.INFO, 'Upload from above file formats only.')
    
    return render(request,'home.html')
def choose(request):
    if request.method=='POST':
        radoption = request.POST["option"]
        if radoption=="report":
            return HttpResponseRedirect('/uploadd/')
        else:
            return HttpResponseRedirect('/showw/')
    return render(request,'choose.html')
def show(request):
    if request.method=='POST':
        db=MySQLdb.connect("localhost","root","shreya","up")
        mouse=db.cursor()
        country_name=request.POST['country']
        date_of_report=request.POST['number']
        date_of_report2=request.POST['number2']
        mygraph=request.POST['graph']
        x_axis=request.POST['parax']
        y_axis=request.POST['paray']
        #Selecting the records which r between the given year and have specified country
        sqlquery='select year,max(version) from mydatabase where country=%s and year between %s and %s group by year'
        mouse.execute(sqlquery,[(country_name),(date_of_report),(date_of_report2)])
        results = mouse.fetchall()
        MYLIST=[]
        if results:
            for i in results:
                YEAR=i[0]
                VERSION=i[1]
                print(YEAR,VERSION)
                if int(VERSION)==0:
                   FILENAME=str(country_name)+" "+str(YEAR)+" "+"Sales.csv"
                else:
                   FILENAME=str(country_name)+" "+str(YEAR)+" "+"Sales"+"_"+str(VERSION)+".csv"
                MYLIST+=['E://CODING//project//csv_files//'+str(FILENAME)]
            print(MYLIST)
            #To read a single file from specified location: df=pd.read_csv('E://CODING//project//csv_files//'+country_name+' '+date_of_report+' '+'Sales.csv')
            df = pd.concat(map(pd.read_csv,MYLIST),ignore_index=True)#ignore index given and number it accordingly after concatenating
            print(df)
            
            if mygraph=="SCATTER PLOT":
                fig=px.scatter(df,x=x_axis,y=y_axis, title=str(country_name))
            elif mygraph=="LINE GRAPH":
                fig = px.line(df, x = x_axis, y = y_axis, title="Sales data of "+str(country_name)+" over the year "+str(date_of_report)+" - "+str(date_of_report2))
            elif mygraph=="AREA CHART":
                fig = px.area(df, x=x_axis, y=y_axis, color=x_axis,line_group=y_axis, title="Sales data of "+str(country_name)+" over the year "+str(date_of_report)+" - "+str(date_of_report2))
            elif mygraph=="BAR GRAPH":
                fig=px.bar(df,x=x_axis,y=y_axis,title="Sales data of "+str(country_name)+" over the year "+str(date_of_report)+" - "+str(date_of_report2))
            elif mygraph=="FUNNEL PLOT":
                fig=px.funnel(df,x=x_axis,y=y_axis,title="Sales data of "+str(country_name)+" over the year "+str(date_of_report)+" - "+str(date_of_report2))
            elif mygraph=="PIE CHART":
                fig = px.pie(df, values=x_axis, names=y_axis, title="Sales data of "+str(country_name)+" over the year "+str(date_of_report)+" - "+str(date_of_report2))
            elif mygraph=="DENSITY HEATMAP":
                fig = px.density_heatmap(df, x=x_axis, y=y_axis)
            elif mygraph=="DENSITY CONTOUR":
                fig = px.density_contour(df, x=x_axis, y=y_axis)
            fig.show()
                
            return HttpResponseRedirect('/thankyouuu/')
        else:
           messages.add_message(request, messages.INFO, 'Incorrect data inputted!')
    return render(request,'results.html')
def afterupload(request):
    if request.method=='POST':
        mychoice=request.POST['choice']
        print(mychoice)
        if mychoice=="report":
            return HttpResponseRedirect('/uploadafile/')
        elif mychoice=="generate":
            return HttpResponseRedirect('/gerneratereports/')
    return render(request,'thankyou.html')
def plotgraph(request):
    return render(request,'graphs.html',{'chart':chart})
