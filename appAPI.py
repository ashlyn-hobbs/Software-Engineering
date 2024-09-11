########################################################################
################# S T A R T E R   C O D E ##############################
########################################################################

# Import libraries
from flask import Flask, jsonify, request
from flask_restful import Resource, Api
import requests
import json
import os

# Create the Flask app
app = Flask(__name__)

# Create an API object
api = Api(app)

# This decorator will require an API key to be provided through the header.
def require_api_key(func):
    def wrapper(*args, **kwargs):
        api_key = request.headers.get('api-key')

        if api_key == 'apiproject':
            return func(*args, **kwargs)
        else:
            return jsonify({'message': 'Invalid API key.'})

    return wrapper

# Create Hello resource
class Hello(Resource):

	# corresponds to the GET request.
	@require_api_key
	def get(self):

		return jsonify({'message': 'Hello!'})

########################################################################

# Find your resource below to modify your code!


# Create Person 1 resource
class Resource1(Resource):

	# corresponds to the GET request.
	@require_api_key
	def get(self):

		return jsonify({'message': 'Resource 1 Endpoint'})

# Create Person 2 resource
class Resource2(Resource):

	# corresponds to the GET request.
	@require_api_key
	def get(self):

		return jsonify({'message': 'Resource 2 Endpoint'})

# Create Person 3 resource
class Resource3(Resource):

	# corresponds to the GET request.
	@require_api_key
	def get(self):

		return jsonify({'message': 'Resource 3 Endpoint'})

# Create Person 4 resource
class Resource4(Resource):

	# corresponds to the GET request.
	@require_api_key
	def get(self):

		return jsonify({'message': 'Resource 4 Endpoint'})

# Add the defined resources along with their corresponding urls
api.add_resource(Hello, '/')

api.add_resource(Resource1, '/Resource1')
######################################
# Person 1 additional resources here #

######################################

api.add_resource(Resource2, '/Resource2')
######################################
# Person 2 additional resources here #

######################################

api.add_resource(Resource3, '/Resource3')
######################################
# Person 3 additional resources here #

######################################

api.add_resource(Resource4, '/Resource4')
######################################
# Person 4 additional resources here #

######################################

# Driver function
if __name__ == '__main__':

	app.run(debug = True)