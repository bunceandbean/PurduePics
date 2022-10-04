import tweepy
from datetime import datetime as dt
import requests
from credentials import *

# Authenticate to Twitter
auth = tweepy.OAuthHandler(API_key, API_secret_key)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

#Grab Current Photo String
def get_noon_photo_name() -> tuple:
    now = str(dt.now())
    stamp = now[:now.index(" ")]
    photo_stamp = stamp.replace("-","_")
    photo_name = photo_stamp + "_12_00.jpg"
    web_path = "https://engineering.purdue.edu/ECN/WebCam/cam05/" + photo_name
    readable_stamp = stamp[stamp.index("-")+1:].replace("-","/") + "/" + stamp[:stamp.index("-")].replace("-","/")
    return (web_path, readable_stamp)

time_tuple = get_noon_photo_name()

#Get Current Photo
img_data = requests.get(time_tuple[0]).content
with open('current_photo.jpg', 'wb') as handler:
    handler.write(img_data)

# Make Tweet
try:
    api.verify_credentials()
    api.update_status_with_media(status="Purdue Engineering Mall - " + time_tuple[1] + " @ 12:00pm", filename=filepath+"current_photo.jpg")
    print("Authentication OK")
except:
    print("Error during authentication, logged and stopped scheduling.")
