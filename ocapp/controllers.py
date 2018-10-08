#!/bin/env python3
import re
import requests




class Parser:
    """
    Class created in order to parse the question asked by the user.
    """
    def __init__(self):
        self.question = ''
        self.stopWords = ["!", ",", ".", ";", ":", "?", "salut", "bonjour", "grandpy", "bot", "a", "abord", "absolument", "afin", "ah", "ai", "aie", "ailleurs", "ainsi", "ait", "allaient", "allo", "allons", "allô", "alors", "anterieur", "anterieure", "anterieures", "apres", "après", "as", "assez", "attendu", "au", "aucun", "aucune", "aujourd", "aujourd'hui", "aupres", "auquel", "aura", "auraient", "aurait", "auront", "aussi", "autre", "autrefois", "autrement", "autres", "autrui", "aux", "auxquelles", "auxquels", "avaient", "avais", "avait", "avant", "avec", "avoir", "avons", "ayant", "b", "bah", "bas", "basee", "bat", "beau", "beaucoup", "bien", "bigre", "boum", "bravo", "brrr", "c", "car", "ce", "ceci", "cela", "celle", "celle-ci", "celle-là", "celles", "celles-ci", "celles-là", "celui", "celui-ci", "celui-là", "cent", "cependant", "certain", "certaine", "certaines", "certains", "certes", "ces", "cet", "cette", "ceux", "ceux-ci", "ceux-là", "chacun", "chacune", "chaque", "cher", "chers", "chez", "chiche", "chut", "chère", "chères", "ci", "cinq", "cinquantaine", "cinquante", "cinquantième", "cinquième", "clac", "clic", "combien", "comme", "comment", "comparable", "comparables", "compris", "concernant", "contre", "couic", "crac", "d", "da", "dans", "de", "debout", "dedans", "dehors", "deja", "delà", "depuis", "dernier", "derniere", "derriere", "derrière", "des", "desormais", "desquelles", "desquels", "dessous", "dessus", "deux", "deuxième", "deuxièmement", "devant", "devers", "devra", "different", "differentes", "differents", "différent", "différente", "différentes", "différents", "dire", "directe", "directement", "dit", "dite", "dits", "divers", "diverse", "diverses", "dix", "dix-huit", "dix-neuf", "dix-sept", "dixième", "doit", "doivent", "donc", "dont", "douze", "douzième", "dring", "du", "duquel", "durant", "dès", "désormais", "e", "effet", "egale", "egalement", "egales", "eh", "elle", "elle-même", "elles", "elles-mêmes", "en", "encore", "enfin", "entre", "envers", "environ", "es", "est", "et", "etant", "etc", "etre", "eu", "euh", "eux", "eux-mêmes", "exactement", "excepté", "extenso", "exterieur", "f", "fais", "faisaient", "faisant", "fait", "façon", "feront", "fi", "flac", "floc", "font", "g", "gens", "h", "ha", "hein", "hem", "hep", "hi", "ho", "holà", "hop", "hormis", "hors", "hou", "houp", "hue", "hui", "huit", "huitième", "hum", "hurrah", "hé", "hélas", "i", "il", "ils", "importe", "j", "je", "jusqu", "jusque", "juste", "k", "l", "la", "laisser", "laquelle", "las", "le", "lequel", "les", "lesquelles", "lesquels", "leur", "leurs", "longtemps", "lors", "lorsque", "lui", "lui-meme", "lui-même", "là", "lès", "m", "ma", "maint", "maintenant", "mais", "malgre", "malgré", "maximale", "me", "meme", "memes", "merci", "mes", "mien", "mienne", "miennes", "miens", "mille", "mince", "minimale", "moi", "moi-meme", "moi-même", "moindres", "moins", "mon", "moyennant", "multiple", "multiples", "même", "mêmes", "n", "na", "naturel", "naturelle", "naturelles", "ne", "neanmoins", "necessaire", "necessairement", "neuf", "neuvième", "ni", "nombreuses", "nombreux", "non", "nos", "notamment", "notre", "nous", "nous-mêmes", "nouveau", "nul", "néanmoins", "nôtre", "nôtres", "o", "oh", "ohé", "ollé", "olé", "on", "ont", "onze", "onzième", "ore", "ou", "ouf", "ouias", "oust", "ouste", "outre", "ouvert", "ouverte", "ouverts", "o|", "où", "p", "paf", "pan", "par", "parce", "parfois", "parle", "parlent", "parler", "parmi", "parseme", "partant", "particulier", "particulière", "particulièrement", "pas", "passé", "pendant", "pense", "permet", "personne", "peu", "peut", "peuvent", "peux", "pff", "pfft", "pfut", "pif", "pire", "plein", "plouf", "plus", "plusieurs", "plutôt", "possessif", "possessifs", "possible", "possibles", "pouah", "pour", "pourquoi", "pourrais", "pourrait", "pouvait", "prealable", "precisement", "premier", "première", "premièrement", "pres", "probable", "probante", "procedant", "proche", "près", "psitt", "pu", "puis", "puisque", "pur", "pure", "q", "qu", "quand", "quant", "quant-à-soi", "quanta", "quarante", "quatorze", "quatre", "quatre-vingt", "quatrième", "quatrièmement", "que", "quel", "quelconque", "quelle", "quelles", "quelqu'un", "quelque", "quelques", "quels", "qui", "quiconque", "quinze", "quoi", "quoique", "r", "rare", "rarement", "rares", "relative", "relativement", "remarquable", "rend", "rendre", "restant", "reste", "restent", "restrictif", "retour", "revoici", "revoilà", "rien", "s", "sa", "sacrebleu", "sait", "sans", "sapristi", "sauf", "se", "sein", "seize", "selon", "semblable", "semblaient", "semble", "semblent", "sent", "sept", "septième", "sera", "seraient", "serait", "seront", "ses", "seul", "seule", "seulement", "si", "sien", "sienne", "siennes", "siens", "sinon", "six", "sixième", "soi", "soi-même", "soit", "soixante", "son", "sont", "sous", "souvent", "specifique", "specifiques", "speculatif", "stop", "strictement", "subtiles", "suffisant", "suffisante", "suffit", "suis", "suit", "suivant", "suivante", "suivantes", "suivants", "suivre", "superpose", "sur", "surtout", "t", "ta", "tac", "tant", "tardive", "te", "tel", "telle", "tellement", "telles", "tels", "tenant", "tend", "tenir", "tente", "tes", "tic", "tien", "tienne", "tiennes", "tiens", "toc", "toi", "toi-même", "ton", "touchant", "toujours", "tous", "tout", "toute", "toutefois", "toutes", "treize", "trente", "tres", "trois", "troisième", "troisièmement", "trop", "très", "tsoin", "tsouin", "tu", "té", "u", "un", "une", "unes", "uniformement", "unique", "uniques", "uns", "v", "va", "vais", "vas", "vers", "via", "vif", "vifs", "vingt", "vivat", "vive", "vives", "vlan", "voici", "voilà", "vont", "vos", "votre", "vous", "vous-mêmes", "vu", "vé", "vôtre", "vôtres", "w", "x", "y", "z", "zut", "à", "â", "ça", "ès", "étaient", "étais", "était", "étant", "été", "être", "ô"]
        self.parsedQuestion = ''

    def parse_question(self, question):
        """
        Take the question asked by the user, delete the useless words
        contained in the list stopWords and return the result.
        """
        self.question = question
        tmp = self.question.replace('-', ' ')
        tmp = tmp.replace('\'', ' ')
        tmp = tmp.replace(',', '')
        sentence = tmp.split(' ')

        for word in sentence:
            if word.lower() not in self.stopWords:
                self.parsedQuestion += ' ' + word
        self.parsedQuestion = self.parsedQuestion.strip()
        return self.parsedQuestion
                

    def second_parsing(self):
        """
        In case the first parsing didn't produce any results in the Google Map API, try this.
        For each word, it makes a call to the API Ultralingua. It responds with a list containing
        all the conjugations of the verb if it is a verb, with a dictionnary otherwise.
        If the answer's type is a list, it is not kept from the string.
        """

        #remove all verbs :
        listedQuestion = self.parsedQuestion.split(' ')
        self.parsedQuestion = ''
        url = "http://api.ultralingua.com/api/conjugations/french/"
        for word in listedQuestion:
            link = url + word
            req = requests.get(link)
            if req.status_code == 200:
                res = req.json()
                # if the word is not a verb :
                if isinstance(res, dict):
                    self.parsedQuestion += ' ' + word
                return 0
            else:
                return 1
        return self.parsedQuestion.strip()


    def parse_wiki(self, rawResponse):
        """
        This function take in argument the string returned by the method requestMediaWiki()
        and cleans it from all the hmtl tags. It also takes the first three phrases of the text
        in order to not have a too long text to print on the website.
        """
        cleanr = re.compile('<.*?>')
        cleanText = re.sub(cleanr, '', rawResponse)
        cleanText = cleanText.strip().split('\n')[0]
        cleanText = cleanText.split('.')
        cleanText = '.'.join(cleanText[:3])
        return cleanText


class GoogleMapAPI:
    """
    Class dedicated to the creation of the request to Google Map.
    """
    def __init__(self):
        self.API_KEY = ""
        self.link = ''
        self.lat = -1
        self.lng = -1


    def request_gmap(self, search):
        """
        Take a location in argument, make a request to Google Map API and if status response is OK
        extract the latitude and longitude of the location.
        Two trys are possible, the first one with a simple parsing of the question, the second one
        with another parsing of the question, a bit more harsher.
        """
        self.link = "https://maps.googleapis.com/maps/api/geocode/json?" + \
            "address={place}&region=fr&key=" + \
            self.API_KEY
        self.link = self.link.format(place=search.replace(' ', '+'))
        req = requests.get(self.link)
        
        if req.status_code == 200:
            res = req.json()
            if res['status'] == 'OK':
                self.lat = res['results'][0]['geometry']['location']['lat']
                self.lng = res['results'][0]['geometry']['location']['lng']
                return 0
            else:
                return 1
        else:
            return -1

    
class MediaWikiAPI:
    """
    Class dedicated to the request to MediaWiki.
    """
    def __init__(self):
        self.idPage = -1
        self.textBot = ''
        self.linkWikipedia = ''

    def get_wiki_page(self, latitude, longitude):
        """
        Take the latitude and longitude returned by the method requestGMAP() and make a request
        to the API MediaWiki with these coordinates. It responds with a list of dictionnary containing
        the id of the wikipedia pages near the coordinates.
        The function extracts the id page of the first page.
        """
        link = "https://fr.wikipedia.org/w/api.php?action=query&list=geosearch&gsradius=10000&gscoord={lat}%7C{lng}&format=json".format(lat=latitude, lng=longitude)
        req = requests.get(link)
        if req.status_code == 200:
            res = req.json()
            if 'error' not in res.keys():
                self.idPage = res['query']['geosearch'][0]['pageid']
                return 0
            else:
                return 1
        else:
            return 1
        

    def request_media_wiki(self):
        """
        Make a request to the MediaWiki API and extracts the text of the page.
        """
        link = "https://fr.wikipedia.org/w/api.php?action=query&pageids={page_id}&prop=extracts&rvprop=content&format=json".format(page_id=self.idPage)
        req = requests.get(link)

        if req.status_code == 200:
            res = req.json()
    
            # if no article is found :
            if 'error' not in res.keys():
                self.textBot = res['query']['pages'][str(self.idPage)]['extract']
                self.linkWikipedia = "https://fr.wikipedia.org/wiki/" + \
                    res['query']['pages'][str(self.idPage)]['title'].replace(' ', '_')
                return 0    
            else:
                return 1
        else:
            return 1
        

def main():
    #question = input('Entrez votre question : ')
    question = "Salut GrandPy, tu connais l'addresse d'Openclassrooms ?"
    
    #Parse the question
    parser = Parser()
    search = parser.parse_question(question)
    gmap = GoogleMapAPI()
    count = 1

    if gmap.request_gmap(search, count) == 1:
        count += 1
        search = parser.second_parsing()
        if gmap.request_gmap(search, count) == 1:
            print("Désolé mon petit, je n'ai rien trouvé, es-tu sûr de l'orthographe ?")
            return

    #Find an article about it on Wikipedia
    wiki = MediaWikiAPI()
    if wiki.get_wiki_page(gmap.lat, gmap.lng) == 1:
        print("Désolé mon petit, je ne me souviens de rien concernant cet endroit.")
    else:
        textBot, link = wiki.request_media_wiki()
        textBot = parser.parse_wiki(wiki.textBot)
        print("lat : ", gmap.lat)
        print("lng : ", gmap.lng)
        print("\n", textBot)
        print(link)


if __name__ == "__main__":
    main()