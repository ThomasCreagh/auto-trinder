from lib import TrinderImage
import pygsheets
from datetime import datetime
import os

client = pygsheets.authorize(service_account_file="auto-trinder-e79abbfcea61.json") 
spreadsheet = client.open(client.spreadsheet_titles()[0]) 

wks = spreadsheet.sheet1
cwd = os.getcwd()
title = True
for row in wks:
    name = row[0].replace("/", "-").replace(" ", "-")
    if title: 
        title = False
        continue

    dir_list = os.listdir(cwd+"/output")
    if f"{name}.png" not in dir_list:
        TrinderImage(row[2],
                    "data/background.jpeg",
                    "data/Arial.ttf",
                    f"output/{name}.png")
