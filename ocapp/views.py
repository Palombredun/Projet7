#!/bin/env python3

from flask import Flask, jsonify, render_template, request  

from ocapp import main as script


app = Flask(__name__)

# Config options - Make sure you created a 'config.py' file.
#app.config.from_object('config')
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
        result = script.treat_question(question)
    
        if isinstance(result, tuple):
            lat = result[0]
            lng = result[1]
            textBot = result[2]
            linkWiki = result[3]
            API_KEY = result[4]
            with open("ocapp/templates/map.html", "r") as f:
                text = f.read()
            with open("../..temp.html", "w") as g:
                g.write(text.format(\
                    textBot=textBot, linkWiki=linkWiki,\
                    latitude=lat, longitude=lng, API_KEY=API_KEY))
            #return jsonify({'res': render_template('gmap.html', textBot=textBot, linkWiki=linkWiki, \
            #    latitude=lat, longitude=lng, API_KEY=API_KEY)})
            return '0'
        else:
            with open("ocapp/templates/error.html", "r") as f:
                text = f.read()
            with open("ocapp/templates/temp.html", "w") as g:
                g.write(text.format(error_message=result))
            #return render_template('error.html', error_message=result)
            return '0'

if __name__ == "__main__":
    app.run()