from secrets import client_id, redirect_uri
from urllib.parse import urlencode, quote

def generateURL():
        parameters = {'client_id': client_id, 'response_type': 'code', 'redirect_uri': redirect_uri, 'scope': 'playlist-modify-public playlist-modify-private'}
        endpoint = "https://accounts.spotify.com/authorize"
        queryParameters = urlencode(parameters, quote_via=quote)
        return "{}?{}".format(endpoint, queryParameters)
print(generateURL())