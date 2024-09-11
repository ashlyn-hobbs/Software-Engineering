########################################################################
################# S T A R T E R   C O D E ##############################
########################################################################

# Import libraries
from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse
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

		# creates the parser for obtaining the API argument "type" and reads into arguments
		parser = reqparse.RequestParser()
		parser.add_argument("type", type=str, location='args')
		arguments=parser.parse_args()

		playlist_access_token = "BQD8aRGz8_YapQuPXWMZaDRsajwChBezgqKVhgd7FaRZgPwMzcmf3RCkXW11E2ytf5ObCrxo_yOQJlnTzeI8FAOiGRfnmInGcNU6bmBGMhuC6AkkwLw"
		# Define the headers with the bearer token
		headers = {'Authorization': f'Bearer {playlist_access_token}' }

		# depending on the "type" being either "inspire", "stoic", or "random",
		# chooses one of three APIs to pull a quote from
		if arguments["type"] == "Study":
			playlist_url = ("https://api.spotify.com/v1/playlists/37i9dQZF1EIfMdgv54LYV9")
		elif arguments["type"] == "Classical":
			playlist_url = ("https://api.spotify.com/v1/playlists/37i9dQZF1DWWEJlAGA9gs0")
		elif arguments["type"] == "Motivational":
			playlist_url = ("https://api.spotify.com/v1/playlists/37i9dQZF1EIh4zcdX2LJPS")
		elif arguments["type"] == "Heartbreak":
			playlist_url = ("https://api.spotify.com/v1/playlists/37i9dQZF1EIeSXgC3Z17tF")
		elif arguments["type"] == "Karaoke":
			playlist_url = ("https://api.spotify.com/v1/playlists/37i9dQZF1EIdf4FT0py4jy")
		elif arguments["type"] == "Party":
			playlist_url = ("https://api.spotify.com/v1/playlists/37i9dQZF1EIdzRg9sDFEY3")
		else:
			return jsonify({"message": "Please pick from one of the avaliable playlists: Study, Classical, Motivational, Heartbreak, Karaoke or Party"})

		# Send GET request to Spotify API with the appropriate URL and headers
		playlist_response = requests.get(playlist_url, headers=headers)

        # Check if request was successful
		if playlist_response.status_code == 200:
            # Return the API response in JSON format
			return jsonify(playlist_response.json())
		else:
			return jsonify({"message": "Failed to fetch playlist data"}), playlist_response.status_code

# Create Person 2 resource
class SpotifySearch(Resource):

    @require_api_key
    # corresponds to the GET request
    def get(self):
        # Hardcoded access token for Resource 2
        access_token = 'BQA1YI3PteZY4y8mDtBvC7l844rRP3Tx0NLe5IAVPcuC5BxDfSUKemOWKoXNqaeYc-SYNRoZQylgNCwoGKTjxFWyp8J2qV0zx-5kwQLdNx0-E7lIut4'

        # Construct the headers with the access token
        headers = {'Authorization': f'Bearer {access_token}'}

        # Get parameters from the query string
        query = request.args.get('q')
        type = request.args.get('type')  # type can be 'artist', 'album', or 'track'

        # Construct the URL for the Spotify API with the query parameter
        url = f'https://api.spotify.com/v1/search?q={query}&type={type}'

        # Make a GET request to the Spotify API
        response = requests.get(url, headers=headers)

        return jsonify(response.json())

# Create Person 3 resource
class Resource3(Resource):

	# corresponds to the GET request.
	@require_api_key
	def get(self):

		# creates the parser for obtaining the API argument "type" and reads into arguments
		parser = reqparse.RequestParser()
		parser.add_argument("type", type=str, location='args')
		arguments=parser.parse_args()

		# depending on the "type" being either "inspire", "stoic", or "random",
		# chooses one of three APIs to pull a quote from
		if arguments["type"] == "inspire":
			quote = requests.get("http://api.forismatic.com/api/1.0/?method=getQuote&lang=en&format=json")
		elif arguments["type"] == "stoic":
			quote = requests.get("https://stoic.tekloon.net/stoic-quote")
		elif arguments["type"] == "random":
			quote = requests.get("https://zenquotes.io/api/random/")
		else:
			return jsonify({"message": "Please use only 'inspire', 'stoic', or 'random' for the 'type' argument"})

		# returns the API response in json format
		return jsonify(quote.json())

# Create Person 4 resource
class AnimalPictures(Resource):

	# corresponds to the GET request.
	@require_api_key
	def get(self):

        #creates parser for obtaining the API arguement "animal" and loads into arguments
		parser = reqparse.RequestParser()
		parser.add_argument("animal",type = str, location = 'args')
		argument = parser.parse_args()

        #api data from https://dog.ceo/dog-api/documentation/, https://shibe.online/
        #depending on the animal argument pull from various APIs for each animal
       
		if argument['animal'] == "dog":
			picture = requests.get('https://dog.ceo/api/breeds/image/random')
		elif argument['animal'] == "cat":
			picture = requests.get('https://shibe.online/api/cats?count=1')
		elif argument['animal'] == "bird":
			picture = requests.get('https://shibe.online/api/birds?count=1')
		else:
			return jsonify({"message": "Please only use 'dog','cat', or 'bird' for the 'animal' parameter"})

		return jsonify(picture.json())
	
# Add the defined resources along with their corresponding urls
api.add_resource(Hello, '/')

api.add_resource(Resource1, '/Resource1')
######################################
# Person 1 additional resources here #

######################################

api.add_resource(SpotifySearch, '/Resource2')
######################################
# Person 2 additional resources here #

######################################

api.add_resource(Resource3, '/Resource3')
######################################
# Person 3 additional resources here #

######################################

api.add_resource(AnimalPictures, '/Resource4')
######################################
# Person 4 additional resources here #


######################################

# Driver function
if __name__ == '__main__':

	app.run(debug = True)