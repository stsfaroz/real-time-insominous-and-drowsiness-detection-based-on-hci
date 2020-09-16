

from flask import Flask, render_template, request ,Response, session
app = Flask(__name__)
app.secret_key = 'any random string'
app.config['TEMPLATES_AUTO_RELOAD'] = True
import os
import numpy as np
import cv2
import  imutils
import pytesseract
import pandas as pd
from camera import VideoCamera
import webbrowser
import sqlite3 as sql
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
st="Detecting"
#def ch(st):
 # print("final result is ",st)
  #return st
@app.route('/home',methods=["GET", "POST"])
def home():
   return render_template('home.html')


@app.route('/adlog',methods=["GET", "POST"])
def adlog():
    if request.method == "POST":
            username = request.form["u"]
            password = request.form["p"]
            session['username'] = password
            if username=="admin" and password=="admin":
                return render_template("adlog.html")
            else:
                return render_template("admin.html",result="wrong username or password")
@app.route('/mine')
def mine():
  return render_template("adlog.html")
@app.route('/mine2')
def mine2():
  return render_template("mob.html")
                  


@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
   if request.method == 'POST':
      try:
         mail= request.form['mail']
         car = request.form['car']
         name = request.form['name']
         number = request.form['number']
         password = request.form['pass']
         print("try",mail,car,name,password)
         
         with sql.connect("eye.db") as con:
            cur = con.cursor()
            print("Content-Type")
            cur.execute("INSERT INTO user (gmail,car_no,name,number,password) VALUES (?,?,?,?,?)",(mail,car,name,number,password) )
            
            con.commit()
            msg = "Record successfully added"
      except:
         con.rollback()
         msg = "error in insert operation"
      
      finally:
         return render_template("adlog.html",result = msg)
         con.close()



@app.route('/delete_user',methods=["GET", "POST"])

def delete_user():
   return render_template('delete_user.html',result="")



@app.route('/user',methods=["GET", "POST"])

def user():
   return render_template('user.html',result="")







@app.route('/adminlog',methods=["GET", "POST"])

def adminlog():
   return render_template('adlog.html',result="")



@app.route('/delete',methods=["GET", "POST"])

def delete():
  if request.method == 'POST':
    try:
      mail= request.form['mail']
      with sql.connect("eye.db") as con:
        cur = con.cursor()
        print("Content-Type")
        cur.execute("DELETE from user where gmail = (?)",[request.form['mail']] )
        con.commit()
        msg = ""

    except:
      con.rollback()
      msg = "error in insert operation"

      
    finally:
      print("msg is", msg)
      return render_template("delete_user.html",result = msg)
      con.close()

@app.route('/index',methods=["GET", "POST"])
@app.route("/")

def index():
   return render_template('index.html')

@app.route('/result',methods=["GET", "POST"])
def result():
  #val=ch()
  return render_template("result.html",result=st)

@app.route('/list')
def list():
   con = sql.connect("eye.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from user")
   
   rows = cur.fetchall(); 
   return render_template("list.html",rows = rows)



@app.route('/usec',methods=["GET", "POST"])
def usec():
  try:
    if request.method == 'POST':
      #try:
      pwd= request.form['p']
      num= request.form['n']
      print("password is", pwd)
      with sql.connect("eye.db") as con:
        cur = con.cursor()
        print("Content-Type")
        cur.execute("select car_no,password from user WHERE gmail=(?)",[request.form["u"]])
        con.commit()
        rows = cur.fetchall()
        for row in rows:
          p=row[0]
          n=row[1]
        if n==pwd and p==num:
          msg="successfully logged"
          return render_template("mob.html",result = msg)
        else:
          msg="username or password wrong"
          return render_template("user.html",result = msg)
  except:
    msg="username or password wrong"
    return render_template("user.html",result = msg)




@app.route('/up',methods=["GET", "POST"])
def up():
  if request.method == 'POST':
    try:
      mail= request.form['mail']
      mob= request.form['mob']
      pwd=request.form['pwd']
      print("true is ",mail,mob,pwd)
      with sql.connect("eye.db") as con:
        cur = con.cursor()
        print("Content-Type")
        cur.execute("select gmail,password from user WHERE gmail=(?)",[request.form["mail"]])
        rows = cur.fetchall()
        print("rows", rows)
        for row in rows:
          m=row[0]
          p=row[1]
        print("values are ",p)
        if pwd==p :
          msg="successfully logged"
          cur.execute("update user set number = ? where gmail = ? ",(mob,mail))
          rows = cur.fetchall()
          print(rows)
          con.commit()
          return render_template("mob.html",result = "updated successfully")
        else:
          msg="username or password wrong"
        return render_template("mob.html",result = msg)
    except:
        return render_template("mob.html",result = "error")
    finally:
        pass





@app.route('/final',methods=["GET", "POST"])
def final():
  return render_template("result.html",result=st)



@app.route('/mob',methods=["GET", "POST"])
def mob():
  return render_template("mob.html",result=st)



@app.route('/admin',methods=["GET", "POST"])
def admin():
  return render_template("admin.html")

@app.route("/logout")         
def logout():
  session.pop('username', None)
  return render_template('index.html')

def gen(camera):
    
    while True:
        global st
        frame = camera.get_frame()
        f2=open("log.txt","r")
        vv=f2.read()
        f2.close()
        if vv==None:
            vv=0
        n=int(vv)
        st="Detecting"

        if n==1:
          st="Drowsiness_Detected"
        print("n value is ", n)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():

    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')




TEMPLATES_AUTO_RELOAD = True


if __name__ == '__main__':
   app.run(debug = True)













































