#!/bin/env python3
import os
from boto.s3.connection import S3Connection

from ocapp.controllers import *
#import ocapp.config as config

def treat_question(question):
    """
    Function parsing the question asked by the user and making the requests to the APIs.
    Returns ERROR if an error occured, else it returns the latitude, longitude, text and
    link wikipedia required for the program to work.
    """
    parser = Parser()   
    search = parser.parse_question(question)
    gmap = GoogleMapAPI()
    gmap.API_KEY = S3Connection(os.environ['API_KEY'])
    
    if gmap.request_gmap(search) is -1:
        return "ERROR"

    else:
        if gmap.request_gmap(search) is False:

            search = parser.second_parsing()
            if isinstance(search, str):
                if gmap.request_gmap(search) is False:
                    return "ERROR"

            else:
                # ultralingua down
                return "ERROR"

        #Find an article about it on Wikipedia
        wiki = MediaWikiAPI()

        if wiki.get_wiki_page(gmap.lat, gmap.lng) is False:
            return "ERROR"
        
        else:
            response = wiki.request_media_wiki()
            if response is False:
                return "ERROR"
            else:
                textBot = parser.parse_wiki(wiki.textBot)
                return (gmap.lat, gmap.lng, textBot, wiki.linkWikipedia, gmap.API_KEY)


if __name__ == "__main__":
    main()