import numpy as np
import pandas as pd
from flask import Flask, request, jsonify, render_template,redirect, url_for, session,Response 
import pickle

import requests
import time
import json

from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)

#databse connection datas
app.secret_key = "rafasafa"

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'rafasafa'
app.config['MYSQL_DB'] = 'patient'
 
print("Sucessfully connected")

mysql = MySQL(app)
'''
url="https://thingspeak.com/channels/2091780/feeds/last.json?api_key=F2BEH7B2BK6ST3W9"
response=requests.get(url)
data_disc=json.loads(response.text)
fetch_glucose=data_disc['field1']
print("Glucose",fetch_glucose)
print(":",data_disc['field2'])
'''

model = pickle.load(open('model.pkl', 'rb'))

dataset = pd.read_csv('diabetes.csv')

dataset_X = dataset.iloc[:,[1, 2, 5, 7, 0]].values

from sklearn.preprocessing import MinMaxScaler
sc = MinMaxScaler(feature_range = (0,1))
dataset_scaled = sc.fit_transform(dataset_X)


@app.route('/')

def home1():
     return render_template('login.html')

@app.route('/login', methods =['GET', 'POST'])
def login():
	msg = ''
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		session["user"]=request.form.get('username')
		print(session["user"])

		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM USER WHERE user = % s AND pass = % s', (username, password, ))
		account = cursor.fetchone()

		if account:
			session['loggedin'] = True
			session['id'] = account['id']
			session['user'] = account['user']
			print("ok")
			msg = username
			return redirect(url_for('home',username = msg))
			return render_template('home.html', username = msg )
		elif not username or not password:
			msg = 'Please fill out the form !'		
		else:
			msg = 'Incorrect username / password !'
	
	elif request.method == 'POST':
		msg = 'Please fill out the form !'
	return render_template('login.html', invalied = msg)




@app.route('/home')
def home():
	
	msg = session["user"]
	return render_template('home.html',username = msg)


@app.route('/feedback', methods =['GET', 'POST'])
def feedback():
	
	msg = ''
	if request.method == 'POST':

		name = request.form['name']
		email = request.form['email']
		no = request.form['no']
		message = request.form['Message']

		if not name or not email or not no:
			msg = 'Please fill out the form !'

		elif not re.match(r'[A-Za-z]+', name):
			msg = 'Name should only contain Letters!'
		
		elif not re.match(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', email):
			msg = 'Invalid email address!'
		elif not re.match(r'[0-9]+', no):
			msg = 'Number Should only Digits!'
		elif not re.match(r'^\d{10}$', no):
			msg = 'Phone number should be exactly 10 digits!'
		else:
			cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
			cursor.execute('INSERT INTO feedback VALUES (% s, % s, % s, % s)', (name,email,no,message))
			mysql.connection.commit()		
			msg = 'Thank you! Your submission has been received!'
			
	elif request.method == 'POST':
		msg = 'Please fill out the form !'
	return render_template('contact.html',answer = msg)
		
@app.route('/about')
def about():
	return render_template('about.html')


@app.route('/predict1')
def predict1():
	return render_template('predict1.html')


@app.route('/index')
def index():
		
		url="https://thingspeak.com/channels/2091780/feeds/last.json?api_key=F2BEH7B2BK6ST3W9"
		response=requests.get(url)
		data_disc=json.loads(response.text)
		fetch_glucose=data_disc['field1']
		fetch_bp=data_disc['field2']
		print("Glucose",fetch_glucose)
		print("BP:",data_disc['field2'])
		return render_template('index.html',glucose=fetch_glucose , bp=fetch_bp)


@app.route('/past')
def past():
    user = session["user"]
    username = user
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM data WHERE username = %s', (username,))
    data = cursor.fetchall()
    if not data:
        test=0
        return render_template('past1.html', account=test,user=username)
    else:
            return render_template('past1.html', account=data)

@app.route('/signup', methods =['GET', 'POST'])
def signup():
	msg = ''
	if request.method == 'POST':

		name = request.form['name']
		username = request.form['username']
		password = request.form['password']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM user WHERE user = % s', (username, ))
		account = cursor.fetchone()
		if account:
			msg = 'Account already exists !'

		elif not username or not password or not name:
			msg = 'Please fill out the form !'

		elif not re.match(r'[A-Za-z]+', name):
			msg = 'name must contain only characters!'

		elif not re.match(r'[A-Za-z0-9]+', username):
			msg = 'Username must contain only characters and numbers !'

		elif (len(password) < 6):
			msg= 'password should be at least 6'

		elif (len(password) > 10):
			msg= 'password should be at maximum 10'	
		
		else:
			cursor.execute('INSERT INTO user VALUES (NULL, % s, % s, % s)', (name,username,password))
			mysql.connection.commit()
			msg = 'You have successfully registered !'
			#cursor.execute('CREATE TABLE %s (id int AUTO_INCREMENT PRIMARY KEY,username varchar(20) NOT NULL,glucose int,bp int,height int,weight int,age int,pregnancy int,logindate datetime default now())',(username))
			#mysql.connection.commit()
	elif request.method == 'POST':
		msg = 'Please fill out the form !'
	return render_template('signup.html',invalied = msg)




@app.route('/predict',methods=['POST'])
def predict():
	if request.method == 'POST':
		
		glucose = request.form.get('glucose')
		if not glucose:
			url="https://thingspeak.com/channels/2091780/feeds/last.json?api_key=F2BEH7B2BK6ST3W9"
			response=requests.get(url)
			data_disc=json.loads(response.text)
			fetch_glucose=data_disc['field1']
			glucose=fetch_glucose
		else:
			glucose = float(request.form['glucose'])
		
		bp = request.form.get('bp')
		if not bp:
			url="https://thingspeak.com/channels/2091780/feeds/last.json?api_key=F2BEH7B2BK6ST3W9"
			response=requests.get(url)
			data_disc=json.loads(response.text)
			fetch_bp=data_disc['field2']
			bp=fetch_bp
		else:
			bp = float(request.form['bp'])

		weight = float(request.form['weight'])
		height = float(request.form['height'])
		meter = height / 100
		square  = meter * meter
		bmi = weight / square
		age = int(request.form['age'])
		preg = int(request.form['pregnancy'])	
		print("BMI = ",round(bmi,2))
		
		data = np.array([[ glucose, bp, bmi, age, preg]])
        
		prediction = model.predict( sc.transform(data) )

		if prediction == 1:
			pred = "Diabetes"
		elif prediction == 0:
			pred = "No Diabetes"
		output = pred
		user=session["user"]
		
		username=user
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('INSERT INTO data VALUES (now(),0,%s,%s,%s,%s,%s,%s,%s,%s)', (username,glucose,bp,weight,height,age,preg,pred))
		mysql.connection.commit()

		gfr = 175 * pow(1.2 , -1.154) * pow(age, -0.203) * 1.2 * 1	

		if(gfr<15 ):
			chance="50 % (Kidney failure)"

		elif(gfr > 90 ):
			chance="10 % (Normal)"

		elif(gfr>60 ):
			chance="10 % (mild decrease)"

		elif(gfr>45):
			chance="20 % (mild to moderate decrease)"

		elif(gfr>15 ):
			chance="30 % (severe decrease)"			

		return render_template('results.html', prediction=prediction,chance=chance)
	    
	'''
        GFR = 175 * (SCr)^(-1.154) * (age)^(-0.203) * (0.742 if female) * (1.212 if African American)

where SCr is the serum creatinine value, and age is the age in years. 
The output of the program is the GFR value calculated based on the provided input values.

If the GFR value is above 90 ml/min/1.73m^2, it is considered normal. 
If the GFR value is less than 60 ml/min/1.73m^2 for three or more months, 
it indicates the presence of kidney disease. 
The severity of kidney disease is classified into stages based on the GFR value, as follows:


Stage 1: GFR > 90 ml/min (normal or high)
Stage 2: GFR = 60-89 ml/min (mild decrease)
Stage 3a: GFR = 45-59 ml/min (mild to moderate decrease)
Stage 3b: GFR = 30-44 ml/min (moderate to severe decrease)
Stage 4: GFR = 15-29 ml/min (severe decrease)
Stage 5: GFR < 15 ml/min (kidney failure)


Therefore, if the GFR value calculated by the program is above 90 ml/min/1.73m^2,
 it indicates normal kidney function. If the GFR value is between 60-89 ml/min/1.73m^2, 
 it is Stage 2 kidney disease, and if it is below 60 ml/min/1.73m^2,
   it indicates more severe kidney disease.

'''

@app.route('/logout')
def logout():
    session.clear()  # Clear the session data
    session['log'] = ""
    return '''<script>alert("You Are Logged Out");window.location="/"</script>'''


if __name__ == "__main__":
    app.run(debug=True)
