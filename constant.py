try:
	from config import APIKEY, CX, TOKEN
except:
	print "Error importing \'config.py\'"
	exit(0)


GOOGLE_URL = "https://www.googleapis.com/customsearch/v1?key=" + APIKEY + "&cx=" + CX + "&fields=items(title,link)&q="

TWITTER_URL = "https://api.twitter.com/1.1/search/tweets.json?count=1&q="

DUCK_URL = "http://api.duckduckgo.com/?format=json&q="

ACCESS_TOKEN = TOKEN

REQUEST_TO = ['google', 'twitter', 'duckduckgo']
