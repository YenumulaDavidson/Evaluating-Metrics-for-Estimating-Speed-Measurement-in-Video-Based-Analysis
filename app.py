from gevent.pywsgi import WSGIServer
import argparse
import os

from flask import Flask, render_template, request
import numpy as np

from ultralytics import YOLO
import argparse
import io
import os
from PIL import Image
import datetime

import torch
from flask import Flask, render_template, request, redirect
import io
from operator import truediv
import os
import json
from PIL import Image
import pandas as pd
import numpy as np
import pickle

import random
import torch
from flask import Flask, jsonify, url_for, render_template, request, redirect


import smtplib 
from email.message import EmailMessage
from datetime import datetime
from werkzeug.utils import secure_filename
import sqlite3

import smtplib 
from email.message import EmailMessage
from datetime import datetime


app = Flask(__name__)
app.config["PATH_TO_UPLOAD"] = os.path.join("static", "img")

RESULT_FOLDER = os.path.join('static')
app.config['RESULT_FOLDER'] = RESULT_FOLDER
DATETIME_FORMAT = "%Y-%m-%d_%H-%M-%S-%f"

model_8 = YOLO('best.pt')  # force_reload = recache latest code



@app.route('/index')
def index():
	return render_template('index.html')

@app.route("/predict", methods=["POST","GET"])
def predict():

    if request.method == "POST":
    
        file = request.files["file"]
        #print(type(val))
        #print(type(file))
        
        print('Model 8')
            
        img_bytes = file.read()
        img = Image.open(io.BytesIO(img_bytes))
        results = model_8(img)
        res_plotted = results[0].plot()
        for result in results:
            boxes = result.boxes  # Boxes object for bbox outputs
            masks = result.masks  # Masks object for segmenation masks outputs
            probs = result.probs  # Class probabilities for classification outputs
            
        img_savename = f"static/image1.png"

        Image.fromarray(res_plotted).save(img_savename)
        return redirect(img_savename)
    
    
    return render_template('index.html')
        
    
@app.route('/')
@app.route('/home')
def home():
	return render_template('home.html')

@app.route('/logon')
def logon():
	return render_template('signup.html')

@app.route('/login')
def login():
	return render_template('signin.html')


@app.route("/signup")
def signup():
    global otp, username, name, email, number, password
    username = request.args.get('user','')
    name = request.args.get('name','')
    email = request.args.get('email','')
    number = request.args.get('mobile','')
    password = request.args.get('password','')
    otp = random.randint(1000,5000)
    #print(otp)
    msg = EmailMessage()
    msg.set_content("Your OTP is : "+str(otp))
    msg['Subject'] = 'OTP'
    msg['From'] = "evotingotp4@gmail.com"
    msg['To'] = email
    
    
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login("evotingotp4@gmail.com", "xowpojqyiygprhgr")
    s.send_message(msg)
    s.quit()
    return render_template("val.html")

@app.route('/predict1', methods=['POST'])
def predict1():
    global otp, username, name, email, number, password
    if request.method == 'POST':
        message = request.form['message']
        print(message)
        if int(message) == otp:
            print("TRUE")
            con = sqlite3.connect('signup.db')
            cur = con.cursor()
            cur.execute("insert into `info` (`user`,`email`, `password`,`mobile`,`name`) VALUES (?, ?, ?, ?, ?)",(username,email,password,number,name))
            con.commit()
            con.close()
            return render_template("signin.html")
    return render_template("signup.html")

@app.route("/signin")
def signin():

    mail1 = request.args.get('user','')
    password1 = request.args.get('password','')
    con = sqlite3.connect('signup.db')
    cur = con.cursor()
    cur.execute("select `user`, `password` from info where `user` = ? AND `password` = ?",(mail1,password1,))
    data = cur.fetchone()

    if data == None:
        return render_template("signin.html")    

    elif mail1 == str(data[0]) and password1 == str(data[1]):
        return render_template("index.html")
    else:
        return render_template("signup.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/notebook")
def notebook1():
    return render_template("ObjectDetection.html")


if __name__ == "__main__":
    
    app.run(debug=False)  # debug=True causes Restarting with stat
