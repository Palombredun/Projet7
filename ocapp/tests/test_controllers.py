#!/bin/env python3

import ocapp.controllers as script
import pytest
import requests
import json


################################################
#################### PARSER ####################
################################################

class TestParser:
	parser = script.Parser()
	parser.question = "Salut GrandPy ! Est-ce que tu connais l'adresse d'Openclassrooms ?"

	# get an attribute question :
	def test_question(self):
		assert self.parser.question == "Salut GrandPy ! Est-ce que tu connais l'adresse d'Openclassrooms ?"

	def test_set_question(self):
		self.parser.question = "Voici une question"
		assert self.parser.question == "Voici une question"

	def test_parseQuestion(self):
		self.parser.question = "Salut GrandPy ! Est-ce que tu connais l'adresse d'Openclassrooms ?"
		assert self.parser.parseQuestion(self.parser.question) == "connais adresse Openclassrooms"

	def test_parseWiki(self):
		text = """
				<p>L'<b>Hôtel Bourrienne</b> (appelé aussi <b>Hôtel de Bourrienne</b> et <b>Petit Hôtel Bourrienne</b>) est un hôtel particulier du <abbr class="abbr" title="18ᵉ siècle"><span>XVIII</span><sup style="font-size:72%">e</sup></abbr> siècle situé au 58 rue d'Hauteville dans le <abbr class="abbr" title="Dixième">10<sup>e</sup></abbr> arrondissement de Paris. Propriété privée, il est classé au titre des monuments historiques depuis le <time class="nowrap date-lien" datetime="1927-06-20" data-sort-value="1927-06-20">20 juin 1927</time>. En juillet 2015, il est acheté par l'entrepreneur Charles Beigbeder pour en faire le siège de ses activités d'investissement.</p>
				"""
		assert self.parser.parseWiki(text) == "L'Hôtel Bourrienne (appelé aussi Hôtel de Bourrienne et Petit Hôtel Bourrienne) est un hôtel particulier du XVIIIe siècle situé au 58 rue d'Hauteville dans le 10e arrondissement de Paris. Propriété privée, il est classé au titre des monuments historiques depuis le 20 juin 1927. En juillet 2015, il est acheté par l'entrepreneur Charles Beigbeder pour en faire le siège de ses activités d'investissement"

def test_secondParsing(monkeypatch):
	# The monkeypatch function is defined within the larger test of the function
    def fake_get(api_url):
        # OMG I know this looks bad, but I think it's okay...!
        class Fake_Response(object):
            def __init__(self):
                self.text = '''
                				[{'partofspeech': {
                					'partofspeechcategory': verb
                					}
                				}]
                			'''
            # Faking the requests.Response.json() method
            def json():
                return json.loads(self.text)

        return Fake_Response
    
    parser = script.Parser()
    parser.parsedQuestion = "connais"
    parser.secondParsing()
    monkeypatch.setattr(requests, 'get', fake_get)
    assert parser.parsedQuestion == ''

################################################
##################### GMAP #####################
################################################

class TestGoogleMapAPI:
	gmap = script.GoogleMapAPI()

	def test_API_KEY(self):
		assert self.gmap.API_KEY == ""

	def test_set_API_KEY(self):
		self.gmap.API_KEY = 'ThisIsAnAPI_KEY_864'
		assert self.gmap.API_KEY == "ThisIsAnAPI_KEY_864"

	def test_link(self):
		assert self.gmap.link == ''

	def test_set_link(self):
		self.gmap.link = 'https://google.com'
		assert self.gmap.link == 'https://google.com'

	def test_latitude(self):
		assert self.gmap.lat == -1

	def test_set_latitude(self):
		self.gmap.lat = 48.0641544
		assert self.gmap.lat == 48.0641544

	def test_longitude(self):
		assert self.gmap.lng == -1

	def test_set_longitude(self):
		self.gmap.lng = 84.2126321
		assert self.gmap.lng == 84.2126321

def test_requestGMAP(monkeypatch):
		results = {
			"results": [
			{
				"geometry": {
					"location": {
						"lat": 48.8747578,
						"lng" : 2.3505647
						}
					}
				}
			],
			"status": "OK"
		}
		def mock_return(request):
			class MockResponse:
				def json(self):
					return results
			return MockResponse()

		gmap = script.GoogleMapAPI()
		gmap.requestGMAP('adresse Openclassrooms', 1)     
		monkeypatch.setattr(requests, 'get', results)
		
		assert gmap.lat == 48.8747578
		assert gmap.lng == 2.350564700000001

################################################
##################### WIKI #####################
################################################

class TestMediaWikiAPI:
	wiki = script.MediaWikiAPI()

	def test_idPage(self):
		assert self.wiki.idPage == -1

	def test_set_idPage(self):
		self.wiki.idPage = 84
		assert self.wiki.idPage == 84

	def test_textBot(self):
		assert self.wiki.textBot == ''

	def test_set_textBot(self):
		self.wiki.textBot = "Lorem ipsum is a long text"
		assert self.wiki.textBot == "Lorem ipsum is a long text"

	def test_linkWikipedia(self):
		assert self.wiki.linkWikipedia == ''

	def test_set_linkWikipedia(self):
		self.wiki.linkWikipedia = 'https://wikipedia.org'
		assert self.wiki.linkWikipedia == 'https://wikipedia.org'

#def test_requestMediaWiki(monkeypatch):
#	results = """
#	{'batchcomplete': '', 'query': {'geosearch': [{'pageid': 5091748, 'ns': 0, 'title': 'Hôtel Bourrienne', 'lat': 48.874525, 'lon': 2.3511388888889, 'dist': 49.3, 'primary': ''}, {'pageid': 5653202, 'ns': 0, 'title': 'Cité Paradis', 'lat': 48.87409, 'lon': 2.35064, 'dist': 74.5, 'primary': ''}, {'pageid': 438469, 'ns': 0, 'title': "Rue d'Hauteville", 'lat': 48.874087, 'lon': 2.350645, 'dist': 74.8, 'primary': ''}, {'pageid': 6035646, 'ns': 0, 'title': 'Hôtel Botterel de Quintin', 'lat': 48.8742, 'lon': 2.34989, 'dist': 79.3, 'primary': ''}, {'pageid': 997523, 'ns': 0, 'title': 'Rue des Petites-Écuries (Paris)', 'lat': 48.873699, 'lon': 2.3511521, 'dist': 125.3, 'primary': ''}, {'pageid': 6029848, 'ns': 0, 'title': 'Hôtel Titon', 'lat': 48.8751, 'lon': 2.34842, 'dist': 161.4, 'primary': ''}, {'pageid': 4538146, 'ns': 0, 'title': 'Rue des Messageries', 'lat': 48.876317, 'lon': 2.34983, 'dist': 181.5, 'primary': ''}, {'pageid': 5423183, 'ns': 0, 'title': 'Rue Gabriel-Laumain', 'lat': 48.873374, 'lon': 2.3491, 'dist': 187.5, 'primary': ''}, {'pageid': 5423724, 'ns': 0, 'title': 'Rue Martel', 'lat': 48.874051, 'lon': 2.353048, 'dist': 197.9, 'primary': ''}, {'pageid': 1494003, 'ns': 0, 'title': 'Quartier de la Porte-Saint-Denis', 'lat': 48.8733952, 'lon': 2.3525548, 'dist': 210.1, 'primary': ''}]}}
#	"""
#	def mock_return(request):
#		class MockResponse:
#			def json(self):
#				return results
#		return MockResponse()
#
#	parser = script.MediaWikiAPI()
#	parser.idPage =  5091748
#	textBot, link = parser.requestMediaWiki()     
#	monkeypatch.setattr(requests, 'get', results)
#	test = "LONG TEXT"
#	assert parser.textBot == test#