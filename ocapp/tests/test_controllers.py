#!/bin/env python3

import pytest
import requests
import requests_mock
import json

import ocapp.controllers as script
import config


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


    def test_parse_question(self):
        self.parser.question = "Salut GrandPy ! Est-ce que tu connais l'adresse d'Openclassrooms ?"
        assert self.parser.parse_question(self.parser.question) == "connais adresse Openclassrooms"

    def test_parse_wiki(self):
        text = """
                <p>L'<b>Hôtel Bourrienne</b> (appelé aussi <b>Hôtel de Bourrienne</b> et <b>Petit Hôtel Bourrienne</b>) est un hôtel particulier du <abbr class="abbr" title="18ᵉ siècle"><span>XVIII</span><sup style="font-size:72%">e</sup></abbr> siècle situé au 58 rue d'Hauteville dans le <abbr class="abbr" title="Dixième">10<sup>e</sup></abbr> arrondissement de Paris. Propriété privée, il est classé au titre des monuments historiques depuis le <time class="nowrap date-lien" datetime="1927-06-20" data-sort-value="1927-06-20">20 juin 1927</time>. En juillet 2015, il est acheté par l'entrepreneur Charles Beigbeder pour en faire le siège de ses activités d'investissement.</p>
                """
        assert self.parser.parse_wiki(text) == "L'Hôtel Bourrienne (appelé aussi Hôtel de Bourrienne et Petit Hôtel Bourrienne) est un hôtel particulier du XVIIIe siècle situé au 58 rue d'Hauteville dans le 10e arrondissement de Paris. Propriété privée, il est classé au titre des monuments historiques depuis le 20 juin 1927. En juillet 2015, il est acheté par l'entrepreneur Charles Beigbeder pour en faire le siège de ses activités d'investissement"

def test_second_parsing(monkeypatch):
    def fake_get(api_url):
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
    parser.parsed_question = "connais"
    parser.second_parsing()
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


def test_request_gmap(monkeypatch):
    def fake_get(api_url):
        class Fake_Response(object):
            def __init__(self):
                self.status_code = 200
                self.text = '''
                                {
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
                            '''
            # Faking the requests.Response.json() method
            def json():
                return json.loads(self.text)
        
        return Fake_Response


    monkeypatch.setattr(requests, 'get', fake_get)
    gmap = script.GoogleMapAPI()
    search = 'Openclassrooms'
    assert gmap.request_gmap(search) == 0
    assert gmap.lat == 48.8747578
    assert gmap.lng == 2.350564700000001


#def test_status_not_ok(monkeypatch):
#    def fake_get(api_url):
#        class Fake_Response(object):
#            def __init__(self):
#                with requests_mock.Mocker() as m:
#                    req = m.get('http://test.com', status_code=404)
#                    self.status_code = requests.get('http://test.com').status_code
#
#            def resp():
#                return self.status_code
#        return Fake_Response
#
#    gmap = script.GoogleMapAPI()
#    resp = gmap.request_gmap('adresse Openclassrooms')
#    monkeypatch.setattr(requests, 'get', fake_get)
#    assert resp == 1


    

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

    def test_link_wikipedia(self):
        assert self.wiki.linkWikipedia == ''

    def test_set_link_wikipedia(self):
        self.wiki.linkWikipedia = 'https://wikipedia.org'
        assert self.wiki.linkWikipedia == 'https://wikipedia.org'

def test_get_wiki_page(monkeypatch):
    def fake_get(api_url):
        class Fake_Response(object):
            def __init__(self):
                results = {
                    'batchcomplete': '',
                    'query': {
                        'geosearch': [{
                            'pageid': 509178,
                            'ns': 0,
                            'title': 'Hôtel Bourrienne',
                            'lat': 48.874525,
                            'lon': 2.3511388888889,
                            'dist': 49.3,
                            'primary': ''
                        }]
                    }
                }
            def json(self):
                return str(results)
        return Fake_Response

    lat = 48.8747578
    lng = 2.350564700000001
    wiki = script.MediaWikiAPI()
    assert wiki.get_wiki_page(lat, lng) == 0


def test_request_media_wiki(monkeypatch):
    with open('ocapp/tests/requests.txt', 'r') as f:
        results = f.read()

    def mock_return(request):
        class MockResponse(self):
            def json(self):
                return results
        return MockResponse

    wiki = script.MediaWikiAPI()
    wiki.idPage = 5091748
    textBot, link = wiki.request_media_wiki()
    assert textBot == results
    assert link == "https://fr.wikipedia.org/wiki/Hôtel_Bourrienne"