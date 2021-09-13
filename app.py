from flask import Flask, render_template, url_for, request, redirect  
import mysql.connector

app = Flask(__name__) 

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="passave"
)

def select_pass():
  mycursor = mydb.cursor()
  query = """ SELECT * from password """
  mycursor.execute(query,)
  res = mycursor.fetchall()
  return res

@app.route("/")                   
def index():
  return render_template('login.html', msg="null")


@app.route("/login", methods=['GET', 'POST'])
def login():
  username = request.form.get('username')
  password = request.form.get('password')
  mycursor = mydb.cursor()
  query = """ SELECT * from login where username=%s and password=%s """
  value = (username, password)
  mycursor.execute(query, value)
  res = mycursor.fetchall()
  if(len(res)<1):
    return render_template('login.html', msg="error")

  return redirect('/shortcut')

@app.route("/shortcut")
def shortcut():
  return render_template('index.html', data=select_pass())

@app.route("/add")
def add():
  return render_template('ajouter.html')

@app.route("/add_acount", methods=['GET', 'POST'])
def addAcount():
  type_act = request.form.get('type')
  username = request.form.get('username')
  password = request.form.get('password')
  mycursor = mydb.cursor()
  query = """ INSERT INTO password (type, username, password) VALUES (%s,%s,%s) """
  value = (type_act, username, password)
  mycursor.execute(query, value)
  mydb.commit()
  return redirect('/shortcut')

@app.route("/del/<int:uid>")
def delete(uid):
  mycursor = mydb.cursor()
  query = """ DELETE FROM password where id =%s """
  value = (uid,)
  mycursor.execute(query, value)
  mydb.commit()
  return render_template('index.html', data=select_pass())

if __name__ == "__main__":        
    app.run()  