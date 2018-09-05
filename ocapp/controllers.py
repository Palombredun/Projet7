#!/bin/env python3
import requests
import json
import re



class Parser:
	"""
	Class created in order to parse the question asked by the user.
	"""
	def __init__(self):
		self.question = ''
		self.stopWords = ["!", ",", ".", ";", ":", "?", "salut", "bonjour","grandpy", "bot", "a","abord","absolument","afin","ah","ai","aie","ailleurs","ainsi","ait","allaient","allo","allons","allô","alors","anterieur","anterieure","anterieures","apres","après","as","assez","attendu","au","aucun","aucune","aujourd","aujourd'hui","aupres","auquel","aura","auraient","aurait","auront","aussi","autre","autrefois","autrement","autres","autrui","aux","auxquelles","auxquels","avaient","avais","avait","avant","avec","avoir","avons","ayant","b","bah","bas","basee","bat","beau","beaucoup","bien","bigre","boum","bravo","brrr","c","car","ce","ceci","cela","celle","celle-ci","celle-là","celles","celles-ci","celles-là","celui","celui-ci","celui-là","cent","cependant","certain","certaine","certaines","certains","certes","ces","cet","cette","ceux","ceux-ci","ceux-là","chacun","chacune","chaque","cher","chers","chez","chiche","chut","chère","chères","ci","cinq","cinquantaine","cinquante","cinquantième","cinquième","clac","clic","combien","comme","comment","comparable","comparables","compris","concernant","contre","couic","crac","d","da","dans","de","debout","dedans","dehors","deja","delà","depuis","dernier","derniere","derriere","derrière","des","desormais","desquelles","desquels","dessous","dessus","deux","deuxième","deuxièmement","devant","devers","devra","different","differentes","differents","différent","différente","différentes","différents","dire","directe","directement","dit","dite","dits","divers","diverse","diverses","dix","dix-huit","dix-neuf","dix-sept","dixième","doit","doivent","donc","dont","douze","douzième","dring","du","duquel","durant","dès","désormais","e","effet","egale","egalement","egales","eh","elle","elle-même","elles","elles-mêmes","en","encore","enfin","entre","envers","environ","es","est","et","etant","etc","etre","eu","euh","eux","eux-mêmes","exactement","excepté","extenso","exterieur","f","fais","faisaient","faisant","fait","façon","feront","fi","flac","floc","font","g","gens","h","ha","hein","hem","hep","hi","ho","holà","hop","hormis","hors","hou","houp","hue","hui","huit","huitième","hum","hurrah","hé","hélas","i","il","ils","importe","j","je","jusqu","jusque","juste","k","l","la","laisser","laquelle","las","le","lequel","les","lesquelles","lesquels","leur","leurs","longtemps","lors","lorsque","lui","lui-meme","lui-même","là","lès","m","ma","maint","maintenant","mais","malgre","malgré","maximale","me","meme","memes","merci","mes","mien","mienne","miennes","miens","mille","mince","minimale","moi","moi-meme","moi-même","moindres","moins","mon","moyennant","multiple","multiples","même","mêmes","n","na","naturel","naturelle","naturelles","ne","neanmoins","necessaire","necessairement","neuf","neuvième","ni","nombreuses","nombreux","non","nos","notamment","notre","nous","nous-mêmes","nouveau","nul","néanmoins","nôtre","nôtres","o","oh","ohé","ollé","olé","on","ont","onze","onzième","ore","ou","ouf","ouias","oust","ouste","outre","ouvert","ouverte","ouverts","o|","où","p","paf","pan","par","parce","parfois","parle","parlent","parler","parmi","parseme","partant","particulier","particulière","particulièrement","pas","passé","pendant","pense","permet","personne","peu","peut","peuvent","peux","pff","pfft","pfut","pif","pire","plein","plouf","plus","plusieurs","plutôt","possessif","possessifs","possible","possibles","pouah","pour","pourquoi","pourrais","pourrait","pouvait","prealable","precisement","premier","première","premièrement","pres","probable","probante","procedant","proche","près","psitt","pu","puis","puisque","pur","pure","q","qu","quand","quant","quant-à-soi","quanta","quarante","quatorze","quatre","quatre-vingt","quatrième","quatrièmement","que","quel","quelconque","quelle","quelles","quelqu'un","quelque","quelques","quels","qui","quiconque","quinze","quoi","quoique","r","rare","rarement","rares","relative","relativement","remarquable","rend","rendre","restant","reste","restent","restrictif","retour","revoici","revoilà","rien","s","sa","sacrebleu","sait","sans","sapristi","sauf","se","sein","seize","selon","semblable","semblaient","semble","semblent","sent","sept","septième","sera","seraient","serait","seront","ses","seul","seule","seulement","si","sien","sienne","siennes","siens","sinon","six","sixième","soi","soi-même","soit","soixante","son","sont","sous","souvent","specifique","specifiques","speculatif","stop","strictement","subtiles","suffisant","suffisante","suffit","suis","suit","suivant","suivante","suivantes","suivants","suivre","superpose","sur","surtout","t","ta","tac","tant","tardive","te","tel","telle","tellement","telles","tels","tenant","tend","tenir","tente","tes","tic","tien","tienne","tiennes","tiens","toc","toi","toi-même","ton","touchant","toujours","tous","tout","toute","toutefois","toutes","treize","trente","tres","trois","troisième","troisièmement","trop","très","tsoin","tsouin","tu","té","u","un","une","unes","uniformement","unique","uniques","uns","v","va","vais","vas","vers","via","vif","vifs","vingt","vivat","vive","vives","vlan","voici","voilà","vont","vos","votre","vous","vous-mêmes","vu","vé","vôtre","vôtres","w","x","y","z","zut","à","â","ça","ès","étaient","étais","était","étant","été","être","ô"]
		self.parsedQuestion = ''

	def parseQuestion(self, question):
		"""
		Take the question asked by the user, delete the useless words
		contained in the list stopWords and return the result.
		"""
		self.question = question
		foo = self.question.replace('-', ' ')
		foo = foo.replace('\'', ' ')
		foo = foo.replace(',', '')
		bar = foo.split(' ')

		for word in bar:
			if word.lower() not in self.stopWords:
				self.parsedQuestion += ' ' + word
		self.parsedQuestion = self.parsedQuestion.strip()	
		return self.parsedQuestion
				

	def secondParsing(self):
		"""
		In case the first parsing didn't produce any results, try a harsher one.
		In most cases the problem comes from the verbs, so thanks to an API that replies
		with a list if the word is a verb or a dict if it is not, we can simply delete them.
		"""

		#remove all verbs :
		listedQuestion = self.parsedQuestion.split(' ')
		self.parsedQuestion = ''
		url = "http://api.ultralingua.com/api/conjugations/french/"
		for word in listedQuestion:
			link = url + word
			req = requests.get(link)
			res = req.json()
			# if the word is not a verb : 
			if type(res) == dict:
				self.parsedQuestion += ' ' + word
		return self.parsedQuestion.strip()


	def parseWiki(self, rawResponse):
		"""
		Detect the first structure of the type : == TEXT ==, meaning the next line will contain
		the part that interests us. The function extracts the whole text, clean it and then keep
		only the first two phrases.
		"""
		counter = 0
		expression = r"^(==){1}[ ]{1}"
		print("r = ",len(rawResponse))
		for elt in rawResponse:
			if re.match(expression, elt) is not None:
				break
			else:
				counter += 1
		del rawResponse[:counter]
		text = rawResponse[1]
		# Extracts the first two sentences:
		foo = text.split('.')
		foo = foo[:2]
		chain = '.'.join(foo)

		# remove what used to be links and '[', '{' characters:
		foo = chain.split(' ')
		i = 0
		for i in range(len(foo)):
			if '|' in foo[i] and '{' not in foo[i]:
				tmp = foo[i].find('|')
				foo[i] = foo[i][tmp:]
		i = 0
		for i in range(len(foo)):
			if '|{{' in foo[i]:
				tmp = foo[i].find('|{{')
				foo[i] = foo[i][:tmp]

		text = ' '.join(foo)
		text = text.replace('[', '')
		text = text.replace(']', '')
		text = text.replace('|', '')
		text += '.'
		return text

	def parseAdress(self, formattedAdress):
		expression = r'^[0-9]*[ ]?'
		adress = re.sub(expression, "", formattedAdress)
		i = adress.find(',')
		return adress[:i]


class GoogleMapAPI:
	"""
	Class dedicated to the creation of the request to Google Map. Take the string
	returned by the the function parseQuestion() or secondParsing() and create a
	link with it. 
	"""
	def __init__(self):
		self.base = "https://maps.googleapis.com/maps/api/geocode/json?address="
		self.place = ''
		self.API_KEY = "AIzaSyDuT6k-2LrFv3c0dwPCL83bKwtM0fVM0Jg"
		self.link = ''
		self.location = ''
		self.lat = -1
		self.lng = -1


	def requestGMAP(self, search, count):
		"""
		Create a link and make a request. If the request did not provide a result,
		parse the user's question a second time and repete the request.
		We extract the formatted_adress, the latitude and longitude as well as the place_id
		from the request. The first one will be used, after a bit of parsing for the request to 
		MediaWiki's API and the last three ones for the integration of the map into the website.
		"""
		if count == 1:
			self.place = search
			self.link = self.base + self.place.replace(' ', '+') + "&region=fr&key=" + self.API_KEY
			req = requests.get(self.link)
			res = req.json()
			if res['status'] == 'OK':
				self.location = res['results'][0]['formatted_address']
				self.lat = res['results'][0]['geometry']['location']['lat']
				self.lng = res['results'][0]['geometry']['location']['lng']
				return 0
			else:
				return 1
			
		elif count == 2:
			self.place = search
			self.link = self.base + self.place.replace(' ', '+') + "&region=fr&key=" + self.API_KEY
			req = requests.get(self.link)
			res = req.json()
			if res['status'] == 'OK':
				self.location = res['results'][0]['formatted_address']
				self.lat = res['results'][0]['geometry']['location']['lat']
				self.lng = res['results'][0]['geometry']['location']['lng']
				return 0
			else:
				return 1

	
class MediaWikiAPI:
	"""
	Class dedicated to the request to MediaWiki. The goal is to extract a quote from
	an article about the user's question. If no article is found, just reply with premade
	sentence.
	"""
	def __init__(self):
		self.search = ''
		self.base = "https://fr.wikipedia.org/w/api.php?action=query&titles="
		self.params = "&prop=revisions&rvprop=content&format=json&formatversion=2"
		self.link = ''
		self.text = ''
		self.linkWikipedia = ''

	def requestMediaWiki(self, search):
		"""
		Create a link, make the request, extract a few sentences from the article and print it.
		"""
		self.search = search.replace(' ', '%20')
		self.link = self.base + self.search + self.params
		req = requests.get(self.link)
		res = req.json()

		# if no article is found :
		if 'missing' in res['query']['pages'][0].keys():
			return -1, -1
		
		else:
			foo = res['query']['pages'][0]['revisions'][0]['content']
			self.text = foo.split('\n')
			self.linkWikipedia = "https://fr.wikipedia.org/wiki/" + self.search.replace(' ', '_')
			return self.text, self.linkWikipedia
		

if __name__ == "__main__":
	question = "Salut GrandPy, tu connais l'adresse d'Openclassrooms ?"
	
	parser = Parser()	
	search = parser.parseQuestion(question)
	gmap = GoogleMapAPI()
	count = 1	

	if gmap.requestGMAP(search, count):
		count += 1
		search = parser.secondParsing()
		gmap.requestGMAP(search, count)

	if gmap.requestGMAP(search, count):
		print("Désolé mon petit je n'ai rien trouvé, es-tû sûr de l'orthographe ?")

	searchWiki = parser.parseAdress(gmap.location)
	wiki = MediaWikiAPI()
	text, link = wiki.requestMediaWiki(searchWiki)
	with open('toto.txt', 'w') as f:
		f.write(text[24])

	if text == -1 and link == -1:
		print("Désolé, je ne me souviens de rien à propos de cette endroit.")
	else:
		textBot = parser.parseWiki(text)
	
	print("lat : ", gmap.lat)
	print("lng : ", gmap.lng)
	print("loc : ", gmap.location)
	print("\n", textBot)
	print('\n', link)
