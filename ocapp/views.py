#!/bin/env python3

from flask import Flask, request, render_template, url_for
from jinja2 import Template

from ocapp.controllers import *

app = Flask(__name__)
#with open('gmap.txt', 'r') as file:
#	x = file.read()
#template = Template()
#template.render(lat=lat, lng=lng, API_KEY=API_KEY) 

# Config options - Make sure you created a 'config.py' file.
app.config.from_object('config')
# To get one variable, tape app.config['MY_VARIABLE']

API_KEY = app.config['API_KEY']


@app.route('/', methods=['get', 'post'])
@app.route('/index/', methods=['get', 'post'])
def index():
    if request.method == 'GET':
    	return render_template('index.html')
    elif request.method == 'POST':
    	question = request.form['question']

if __name__ == "__main__":
    app.run()