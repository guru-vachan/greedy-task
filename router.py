from app import app
from flask import request, jsonify, redirect
from datetime import datetime as dt
import gevent
from gevent import monkey
monkey.patch_all()

from exception import InvalidUsage
from helper import get_response, process_command
from constant import REQUEST_TO


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
	response = jsonify(error.to_dict())
	response.status_code = error.status_code
	return response


@app.route('/', methods=['GET'])
def search():
	time = dt.now()
	query = request.args.get('q', None)
	if not query: 
		raise InvalidUsage("Query param \'q\' required.", status_code=400)
	try:
		response = {}
		jobs = []
		response['query'] = query
		response['results'] = {}
		jobs = [gevent.spawn(process_command, x, query, time) for x in REQUEST_TO]
		gevent.joinall(jobs)
		for res in jobs:
			response['results'][res.value[0]] = res.value[1]
		# print 'full', dt.now()-time
		return get_response(response)
	except:	
		raise InvalidUsage("Something happen. Please try again later.", status_code=500)
