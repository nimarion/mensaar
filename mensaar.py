import requests
import pandas as pd
from datetime import datetime
import os
import json

base_url = "https://mensaar.de/api/2/TFtD8CTykAXXwrW4WBU4/1/de/"

def get_base_data():
    url = base_url + "getBaseData"
    response = requests.get(url)
    data = response.json()
    return data

def get_menu(location_id):
    url = base_url + "getMenu/" + str(location_id)
    response = requests.get(url)
    data = response.json()
    return data

    
base_data = get_base_data()
price_tiers = base_data["priceTiers"]

price_tiers = pd.DataFrame(price_tiers)
price_tiers = price_tiers.transpose()
price_tiers.index.names = ["id"]
price_tiers.to_csv("data/price_tiers.csv")

locations = base_data["locations"]
locations = pd.DataFrame(locations)
locations = locations.transpose()
locations.index.names = ["id"]
locations.drop(["description"], axis=1, inplace=True)
locations.rename(columns={"displayName": "name"}, inplace=True)
locations.to_csv("data/locations.csv")

notices = base_data["notices"]
notices = pd.DataFrame(notices)
notices = notices.transpose()
notices.index.names = ["id"]
notices.rename(columns={"displayName": "name"}, inplace=True)
notices.to_csv("data/notices.csv")


location_ids = locations.index.values.tolist()
for location_id in location_ids:
    menu = get_menu(location_id)
    current_date = datetime.now().date()
    current_date = current_date.isoformat() + "T00:00:00.000Z"

    current_day_entry = None
    for day in menu["days"]:
        if day["date"] == current_date:
            current_day_entry = day
            break
    if current_day_entry is None:
        continue

    current_date = datetime.now().date().isoformat()
    directory_path = os.path.join("data", current_date)
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
    

    file_path = os.path.join(directory_path, f"{location_id}.json")
    with open(file_path, "w") as f:
        json.dump(current_day_entry, f, indent=4)
