#!/bin/env python3

from flask import Flask, request, render_template, jsonify 
from jinja2 import Template

from ocapp.controllers import *


app = Flask(__name__)

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
		parser = Parser()	
		search = parser.parseQuestion(question)
		gmap = GoogleMapAPI()
		count = 1	
	
		if gmap.requestGMAP(search, count):
			count += 1
			search = parser.secondParsing()
	
			if gmap.requestGMAP(search, count):
				#return jsonify({'error': "Désolé mon petit je n'ai rien trouvé, es-tû sûr de l'orthographe ?"})
				return jsonify({'lat': -1, 'lng': -1, 'textGrandPy': "Désolé mon petit je n'ai rien trouvé, es-tû sûr de l'orthographe ?", 'linkWiki': link})
		
		searchWiki = parser.parseAdress(gmap.location)
		wiki = MediaWikiAPI()
		text, link = wiki.requestMediaWiki(searchWiki)
	
		if text == -1 and link == -1:
			#return jsonify({'error': "Désolé, je ne me souviens de rien à propos de cette endroit."})
			return jsonify({'lat': gmap.lat, 'lng': gmap.lng, 'textGrandPy': "Désolé, je ne me souviens de rien à propos de cette endroit.", 'linkWiki': link})
		else:
			textGrandPy = parser.parseWiki(text)
		
		with open('toto.txt', 'w') as f:
			f.write(textGrandPy)
		return jsonify({'lat': gmap.lat, 'lng': gmap.lng, 'textGrandPy': textGrandPy, 'linkWiki': link})



if __name__ == "__main__":
	app.run()