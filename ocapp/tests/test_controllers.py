#!/bin/env python3

import ocapp.controllers as script
import pytest
import requests

#def hello(name):
#	return 'hello' + name
#
#def test_hello(name):
#	assert hello('Celine') == 'Hello Celine'

################################################
#################### PARSER ####################
################################################

class TestParser:
	def setup_method(self):
		parser = script.Parser()
		parser.question = "Salut GrandPy ! Est-ce que tu connais l'adresse d'Openclassrooms ?"

	# get an attribute question :
	def test_set_question(self):
		parser = script.Parser()
		parser.question = "Salut GrandPy ! Est-ce que tu connais l'adresse d'Openclassrooms ?"
		assert parser.question == "Salut GrandPy ! Est-ce que tu connais l'adresse d'Openclassrooms ?"

	def test_parseQuestion(self):
		parser = script.Parser()
		parser.question = "Salut GrandPy ! Est-ce que tu connais l'adresse d'Openclassrooms ?"
		assert parser.parseQuestion(parser.question) == "connais adresse Openclassrooms"

	def test_secondParsing(self):
		parser = script.Parser()
		parser.parsedQuestion = "connais adresse Openclassrooms"
		print('print : ',parser.secondParsing())
		assert parser.secondParsing() == "Openclassrooms"

	def test_parseAdress(self):
		parser = script.Parser()
		formattedAdress = '7 Cité Paradis, 75010 Paris, France'
		assert parser.parseAdress(formattedAdress) == 'Cité Paradis'

	def test_parseWiki(self):
		parser = script.Parser()
		req = requests.get("https://fr.wikipedia.org/w/api.php?action=query&titles=Cité%20Paradis&prop=revisions&rvprop=content&format=json&formatversion=2")
		res = req.json()
		rawResponse = res['query']['pages'][0]['revisions'][0]['content'].split('\n')
		assert parser.parseWiki(rawResponse) == "La cité Paradis est une voie publique située dans le 10e arrondissement de Paris de Paris. Elle est en forme de té, une branche débouche au 43, rue de Paradis, la deuxième au 57, rue d'Hauteville et la troisième en impasse."


class TestGoogleMapAPI:
	def test_lat(self):
		gmap = script.GoogleMapAPI()
		place = "Openclassrooms"
		gmap.requestGMAP(place, 1)
		assert gmap.lat == 48.8747578
	
	def test_lng(self):
		gmap = script.GoogleMapAPI()
		place = "Openclassrooms"
		gmap.requestGMAP(place, 1)
		assert gmap.lng == 2.350564700000001
	
	def test_loc(self):
		gmap = script.GoogleMapAPI()
		place = "Openclassrooms"
		gmap.requestGMAP(place, 1)
		assert gmap.location == "7 Cité Paradis, 75010 Paris, France"

class TestMediaWikiAPI:
	def test_text(self):
		wiki = script.MediaWikiAPI()
		search = 'Cité Paradis'
		text, link = wiki.requestMediaWiki(search)

		assert text[24] == """La cité Paradis est une voie publique située dans le [[10e arrondissement de Paris|{{10e|arrondissement}}]] de [[Paris]]. Elle est en forme de [[wikt:té|té]], une branche débouche au 43, [[rue de Paradis]], la deuxième au 57, [[rue d'Hauteville]] et la troisième en impasse."""


	def test_link(self):
		wiki = script.MediaWikiAPI()
		search = 'Cité Paradis'
		text, link = wiki.requestMediaWiki(search)
		assert link == "https://fr.wikipedia.org/wiki/Cité%20Paradis"
