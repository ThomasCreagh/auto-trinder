from lib import TrinderImage
import pygsheets
from datetime import datetime

client = pygsheets.authorize(service_account_file="auto-trinder-e79abbfcea61.json") 
spreadsheet = client.open(client.spreadsheet_titles()[0]) 

wks = spreadsheet.sheet1
title = True
for row in wks:
    if title: 
        title = False
        continue
    
    TrinderImage(row[2],
                  "data/background.jpeg",
                  "data/Arial.ttf",
                  f"output/{datetime.now()}.png")


# print(client.spreadsheet_titles()) 

# test_image = TrinderImage('''Got the assignmet done with 3 mins to spare 😎''',
#                           "data/background.jpeg",
#                           "data/Arial.ttf",
#                           "output/image.png")


