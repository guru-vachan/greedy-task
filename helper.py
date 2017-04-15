import requests
from flask import jsonify
from datetime import datetime as dt

from constant import GOOGLE_URL, TWITTER_URL, DUCK_URL, ACCESS_TOKEN


def process_command(request_to, query, time):
	if request_to == 'twitter':
		return twitter_data(query, time)
	elif request_to == 'google':
		return google_data(query, time)
	else:
		return duck_data(query, time)


def request_header(request_to):
	headers = {
		'accept-encoding': "gzip",
    	'user-agent': "my program (gzip)"
	}
	if request_to == "twitter":
		headers['authorization'] = ACCESS_TOKEN
	return headers


def get_response(data):
	response = jsonify(data)
	response.status_code = 200
	return response


def twitter_data(query, time):
	headers = request_header("twitter")
	url = TWITTER_URL + query
	response = requests.request("GET", url, headers=headers)
	res = {}
	data = response.json()
	try:
		status = data['statuses'][0]
		res['text'] = status['text']
		res['url'] = "https://twitter.com/" + status['user']['screen_name'] + "/status/" + status['id_str']
	except:
		res['message'] = 'No result found.'
	# print 'twitter', dt.now()-time
	return ('twitter', res)


def google_data(query, time):
	headers = request_header("google")
	url = GOOGLE_URL + query
	response = requests.request("GET", url, headers=headers)
	res = {}
	data = response.json()
	try:
		status = data['items'][0]
		res['text'] = status['title']
		res['url'] = status['link']
	except:
		res['message'] = 'No result found.'
	# print 'google', dt.now()-time
	return ('google', res)


def duck_data(query, time):
	headers = request_header("duck")
	url = DUCK_URL + query
	response = requests.request("GET", url, headers=headers)
	res = {}
	data = response.json()
	try:
		if len(data['Results']):
			status = data['Results'][0]
			res['text'] = data['Heading'] + '-' + status['Text']
			res['url'] = status['FirstURL']
		elif data['Heading'] and data['AbstractURL']:
			res['text'] = data['Heading'] + '-' + data['AbstractSource']
			res['url'] = data['AbstractURL']
		else:
			res['message'] = 'No result found.'			
	except:
		res['message'] = 'No result found.'
	# print 'duck', dt.now()-time
	return ('duckduckgo', res)
