#!/bin/env python3

from flask import Flask, jsonify, render_template, request  

from ocapp import main


app = Flask(__name__)

# Config options - Make sure you created a 'config.py' file.
app.config.from_object('config')
# To get one variable, tape app.config['MY_VARIABLE']
#API_KEY = app.config['API_KEY']


@app.route('/')
@app.route('/index/')
def index():
    if request.method == 'GET':
        return render_template('index.html')


@app.route('/results/', methods=['POST'])
def results():
    question = request.form['question']
    content = main(question)

    if isinstance(content, tuple):
        lat = content[0]
        lng = content[1]
        textBot = content[2]
        linkWiki = content[3]
        return jsonify({'map': render_template('gmap.html', textBot=textBot, linkWiki=linkWiki, \
            latitude=lat, longitude=lng, API_KEY=PI_KEY)})
    else:
        return jsonify({'error': render_template('error.html', error_message=content)})

if __name__ == "__main__":
    app.run()