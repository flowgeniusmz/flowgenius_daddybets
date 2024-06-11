import streamlit as st
import pandas as pd
from openai import OpenAI
import requests
import json
import time
from typing import Literal

file_path_odds = "classes2/getdatafun/odds.json"
file_path_events = "classes2/getdatafun/events.json"

def write_json_to_file(json_data, file_path: str):
    with open(file_path, 'w') as file:
        json.dump(json_data, file, indent=4)

def read_json_from_file(file_path: str):
    with open(file_path, 'r') as file:
        json_data = json.load(file)
    return json_data

def get_data_request(type: Literal["odds", "events", "sports"], **kwargs):
    url_template_odds = "https://sportsbook-nash-us{0}.draftkings.com/sites/US-{1}-SB/api/v5/eventgroups/{2}?format=json"
    url_template_events = "https://sportsbook.draftkings.com/sites/US-{0}-SB/api/sportsdata/v1/sports/{1}/events.json"
    url_template_sports = "https://api.draftkings.com/sites/US-DK/sports/v1/sports?format=json"
    
    request_headers = {'Accept': 'application/json','User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36','Accept-Language': 'en-US,en;q=0.9','Accept-Encoding': 'gzip, deflate, br'}

    if type == "odds":
        url = url_template_odds.format(kwargs.get("region_code_lower", "il"), kwargs.get("region_code_upper", "IL"), kwargs.get("event_group_id", "0"))
    elif type == "events":
        url = url_template_events.format(kwargs.get("region_code", "IL"), kwargs.get("sport_id", "0"))
    elif type == "sports":
        url = url_template_sports
    else:
        raise ValueError("Invalid type. Must be one of: 'odds', 'events', 'sports'.")

    response = requests.get(url, headers=request_headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch data from URL: {url} (Status code: {response.status_code})")

# Example usage:
#data = get_data_request("odds", region_code_lower="il", region_code_upper="IL", event_group_id="42133")
#print(data)