import tweepy
from sys import exit
from datetime import datetime as dt
from time import sleep
import requests
from credentials import *

# Authenticate to Twitter
auth = tweepy.OAuthHandler(API_key, API_secret_key)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

#Grab Current Photo String
def get_photo_name(formatted_time: str) -> tuple:
    try:
        now = str(dt.now())
        stamp = now[:now.index(" ")]
        photo_stamp = stamp.replace("-","_")
        photo_name = photo_stamp + formatted_time
        web_path = "https://engineering.purdue.edu/ECN/WebCam/cam05/" + photo_name
        hour = int(formatted_time[1:3])
        am_pm = "am" if hour < 12 else "pm"
        hour = str(hour % 13 + 1) if hour > 12 else str(hour)
        minute = int(formatted_time[4:6])
        minute = "0" + str(minute) if minute == 0 else str(minute)
        clock = hour + ":" + minute + am_pm
        readable_stamp = stamp[stamp.index("-")+1:].replace("-","/") + "/" + stamp[:stamp.index("-")].replace("-","/") + " @ " + clock
        return (web_path, readable_stamp)
    except:
        return (None, None)

#Get Current Photo
def download_image(image_path: str) -> int:
    try:
        img_data = requests.get(image_path).content
        with open(filepath + 'current_photo.jpg', 'wb') as handler:
            handler.write(img_data)
        return 1
    except:
        return 0

#Make Tweet
def make_tweet(stamp: str, filepath: str) -> int:
    try:
        api.verify_credentials()
        api.update_status_with_media(status="Purdue Engineering Mall - " + stamp, filename=filepath + "current_photo.jpg")
        return 1
    except:
        return 0

def main():
    hour = 6
    minute = 50
    for i in range(72):
        minute += 10
        if minute >= 60:
            hour += 1
            minute = 0
        min_str = str(minute)
        hour_str = str(hour)
        if minute == 0:
            min_str = "00"
        if len(hour_str) <= 1:
            hour_str = "0" + hour_str

        photo_name = get_photo_name("_" + hour_str + "_" + min_str + ".jpg")

        if None in photo_name:
            exit("Image Comprehension Failure")

        if not download_image(photo_name[0]):
            exit("Image Download Failure")

        if not make_tweet(photo_name[1], filepath):
            exit("Tweet Creation Failure")

        sleep(600)

if __name__ == "__main__":
    main()
