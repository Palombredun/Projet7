#!/bin/env python3

from flask import Flask, jsonify, render_template, request  

from ocapp import main as script


app = Flask(__name__)

# Config options - Make sure you created a 'config.py' file.
app.config.from_object('config')
# To get one variable, tape app.config['MY_VARIABLE']
#API_KEY = app.config['API_KEY']


@app.route('/')
@app.route('/index/')
def index():
    return render_template('index.html')


@app.route('/results/', methods=['POST'])
def results():
    if request.method == 'POST':
        question = request.form['question']
        content = script.treat_question(question)
    
        if isinstance(content, tuple):
            lat = content[0]
            lng = content[1]
            textBot = content[2]
            linkWiki = content[3]
            with open("toto.txt", "w") as f:
                f.write("toto")
            return jsonify({'res': render_template('gmap.html', textBot=textBot, linkWiki=linkWiki, \
                latitude=lat, longitude=lng, API_KEY=API_KEY)})
        else:
            return jsonify({'error': render_template('error.html', error_message=content)})

if __name__ == "__main__":
    app.run()