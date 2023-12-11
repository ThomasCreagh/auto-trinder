from lib import TrinderImage
import pygsheets
import os
from dotenv import load_dotenv
import json
import requests
from googletrans import Translator


load_dotenv()

API_USER = os.getenv("API_USER")
API_SECRET = os.getenv("API_SECRET")

google_client = pygsheets.authorize(service_account_file="auto-trinder-e79abbfcea61.json") 
spreadsheet = google_client.open(google_client.spreadsheet_titles()[0]) 

wks = spreadsheet.sheet1
cwd = os.getcwd()
title = True


def check_text(text):
    detector = Translator()
    language = detector.detect(text).lang

    if language != "en":
        return False
        
    data = {
        'text': text,
        'mode': 'ml',
        'lang': language,
        'api_user': API_USER,
        'api_secret': API_SECRET
        }
    r = requests.post('https://api.sightengine.com/1.0/text/check.json', data=data)

    output = json.loads(r.text)
    moderation_classes = output["moderation_classes"]["available"]
    for classes in moderation_classes:
        if output["moderation_classes"][classes] > 0.8:
            return False
    return True


for row in wks:
    name = row[0].replace("/", "-").replace(" ", "-")
    if title: 
        title = False
        continue

    dir_list = os.listdir(cwd+"/output")
    bad_dir_list = os.listdir(cwd+"/bad_output")

    if (f"{name}.png" not in dir_list
            and f"{name}.png" not in bad_dir_list):
        text = row[2]
        if check_text(text):
            TrinderImage(text,
                        "data/background.jpeg",
                        "data/Arial.ttf",
                        f"output/{name}.png")
        else:
            TrinderImage(text,
                        "data/background.jpeg",
                        "data/Arial.ttf",
                        f"bad_output/{name}.png")