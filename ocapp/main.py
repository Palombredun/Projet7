#!/bin/env python3

from ocapp.controllers import *

def main(question):
    #Parse the question
    parser = Parser()   
    search = parser.parse_question(question)
    gmap = GoogleMapAPI()
    
    if gmap.request_gmap(search) != -1:
        if gmap.request_gmap(search) == 1:       
            search = parser.second_parsing()
            if isinstance(search, str):
                # no result from gmap
                if gmap.request_gmap(search) == 1:
                    return "Désolé mon petit, je n'ai rien trouvé, es-tu sûr de l'orthographe ?"
            else:
                # ultralingua down
                return "Désolé mon petit, je n'ai rien trouvé, es-tu sûr de l'orthographe ?"

        #Find an article about it on Wikipedia
        wiki = MediaWikiAPI()
        if wiki.get_wiki_page(gmap.lat, gmap.lng) != 1:
            textBot, link = wiki.request_media_wiki()
            textBot = parser.parse_wiki(wiki.textBot)
            # if everything happened fine :
            return(lat, lng, textBot, link) 
        # wiki down
        else:
            return "Désolé mon petit, je ne me souviens de rien concernant cet endroit." 
    # gmap down
    else:
        return "Désolé, je suis en train de m'endormir, tu pourrais repasser dans quelques temps ?"

if __name__ == "__main__":
    main()