import os
import eel
from flask import Flask, request, render_template, redirect, session
from pymongo import MongoClient
import time
from threading import Thread
from chat import *
from command import *
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "testing"

@app.route('/')
def login_signup():
   return render_template('login_signup.html')
 
# Connect to MongoDB
client = MongoClient('mongodb+srv://Ishwar_Gupta:Ishwar123@cluster0.iupts.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client['Ariana']
collection = db['User info']

@app.route('/signup_form', methods=['GET','POST'])
def submit():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm-password']
        if password == confirm_password:
            password = generate_password_hash(password)
        else:
            return render_template('login_signup.html', error="Passwords do not match")

        # Insert data into MongoDB
        data = {
            "username": username,
            "email": email,
            "password":password,
        }
            
        existing_user = collection.find_one({'email':request.form['email']})
        if existing_user is None :
            collection.insert_one(data)
            session['email'] = email
            return render_template('login_signup.html')
        else:
            return render_template('login_signup.html', error="Email already exists")
    
@app.route('/login_form', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        user = collection.find_one({"email": request.form['email']})
            
        if user and check_password_hash(user['password'], request.form['password']):
            # Kill the login window (using taskkill for Edge or your browser)
            os.system("taskkill /F /IM msedge.exe") # Close the browser window
             
            # Start the Eel app for index.html page 
            time.sleep(0.01)# Wait a bit to ensure the login page is closed
            os.system('start msedge "http://localhost:8000/index.html"')
            eel.init('static')  # Path to your static folder
            eel_thread = Thread(target=run_eel)
            eel_thread.start()
            playAssistantSound()
            
            # Redirect to index page (after login)
            return redirect('/index')# Main page
        else:
            return render_template('login_signup.html', error="Incorrect username or password")
            
        
def run_eel():
    eel.start('index.html', mode=None, host='localhost', port="8000", block=True) # Open the index.html page

@app.route('/index')
def index():
    return render_template('index.html')  # Main page after login
            
if __name__ == '__main__':
    # Run the Flask app
    app.run(debug=True, use_reloader=False, port=5000)