import tweepy
import keyring
from googleapiclient import discovery
import json

API_Perspective = "AIzaSyCyl26ferU06eSf6yPWHcmYz1U5IUWQI6M"
# Getting API access securely with keyring
APIKey = keyring.get_password("twitter", "api_key")
APIKeySecret = keyring.get_password("twitter", "api_key_secret")
BearerToken = keyring.get_password("twitter", "bearer_Token")
TOKEN = keyring.get_password("twitter", "token")
TOKEN_SECRET = keyring.get_password("twitter", "token_secret")
# Authenticating into the API
auth = tweepy.OAuthHandler(APIKey, APIKeySecret)
auth.set_access_token(TOKEN, TOKEN_SECRET)
api = tweepy.API(auth)
client = tweepy.Client(bearer_token=BearerToken)

# Getting tweets
# public_tweets = api.home_timeline()
query = "#politica #eleicoes place_country:BR -is:retweet has:geo"
res = client.search_all_tweets(query=query, max_results=100, expansions=["geo.place_id"])

places = {u['id']:u for u in res.includes["places"]}

clientPerspective = discovery.build(
    "commentanalyzer",
    "vlaphal",
    developerKey=API_Perspective,
    discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
    static_discovery=False,
)

for tweet in res.data:
    if places[tweet.geo["place_id"]] is not None:
        place = places[tweet.geo["place_id"]]
        print(tweet)
        analyze_request = {
            'comment': {'text': 'Eu odeio python.'},
            'requestedAttributes': {'TOXICITY': {}}
        }
        response = clientPerspective.comments().analyze(body=analyze_request).execute()
        print(json.dumps(response, indent=2))

# Get tweets around elecion topics

#
