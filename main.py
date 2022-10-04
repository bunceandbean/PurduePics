import tweepy
from credentials import *

# Authenticate to Twitter
auth = tweepy.OAuthHandler(API_key, API_secret_key)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# Make Tweet
try:
    api.verify_credentials()
    api.update_status_with_media(status="Test",filename="/home/bunceandbean/PurduePics/PurduePics/test.jpg")
    print("Authentication OK")
except:
    print("Error during authentication")
