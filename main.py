import tweepy
from credentials import *

# Authenticate to Twitter
auth = tweepy.OAuthHandler(API_key, API_secret_key)
auth.set_access_token(access_token,access_token_secret)

api = tweepy.API(auth)

try:
    api.verify_credentials()
    print("Authentication OK")
    api.update_status_with_media(status="Test",filename="test.jpg")
except:
    print("Error during authentication")
