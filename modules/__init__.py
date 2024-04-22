from datetime import datetime

from flask import Flask, flash, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

