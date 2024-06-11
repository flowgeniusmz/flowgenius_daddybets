import streamlit as st
import pandas as pd
from openai import OpenAI
import requests
import json
import time
from typing import Literal
import datetime

file_path_odds = "classes2/getdatafun/odds.json"
file_path_events = "classes2/getdatafun/events.json"
url_odds = "https://sportsbook-nash-usil.draftkings.com/sites/US-IL-SB/api/v5/eventgroups/42133?format=json"
url_events = "https://sportsbook.draftkings.com/sites/US-IL-SB/api/sportsdata/v1/sports/3/events.json"
request_headers = {'Accept': 'application/json','User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36','Accept-Language': 'en-US,en;q=0.9','Accept-Encoding': 'gzip, deflate, br'}
client = OpenAI(api_key = st.secrets.openai.api_key)
assistantid = st.secrets.openai.assistant_id
assistant = client.beta.assistants.retrieve(assistant_id=assistantid)
current_file_ids = assistant.tool_resources.code_interpreter.file_ids

purpose = "assistants"

def write_json_to_file(json_data, file_path: str):
    with open(file_path, 'w') as file:
        json.dump(json_data, file, indent=4)

def read_json_from_file(file_path: str):
    with open(file_path, 'r') as file:
        json_data = json.load(file)
    return json_data

def create_oai_file(file_path: str):
    file = open(file=file_path, mode="rb")
    oaifile = client.files.create(file=file, purpose=purpose)
    oaifileid = oaifile.id
    return oaifileid

def delete_oai_file(file_id: str):
    client.files.delete(file_id=file_id)

def add_oai_files_to_assistant(file_ids):
    updatevalue = {"code_interpreter": {"file_ids": file_ids}}
    client.beta.assistants.update(assistant_id=assistantid, tool_resources=updatevalue)

def get_request_json(url: str):
    response = requests.get(url=url, headers=request_headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch data from URL: {url} (Status code: {response.status_code})")

def delete_old_files(file_ids):
    for file_id in file_ids:
        client.files.delete(file_id=file_id)

@st.cache_data(ttl=datetime.timedelta(hours=24))
def get_draftkings_data():
    new_file_ids = []
    old_file_ids = current_file_ids

    json_data_odds = get_request_json(url=url_odds)
    write_json_to_file(json_data=json_data_odds, file_path=file_path_odds)
    odds_file_id = create_oai_file(file_path=file_path_odds)
    new_file_ids.append(odds_file_id)

    json_events_data = get_request_json(url=url_events)
    write_json_to_file(json_data=json_events_data, file_path=file_path_events)
    events_file_id = create_oai_file(file_path=file_path_events)
    new_file_ids.append(events_file_id)
    
    print(old_file_ids)
    print(new_file_ids)
    add_oai_files_to_assistant(file_ids=new_file_ids)
    print(client.beta.assistants.retrieve(assistant_id=assistantid))
    delete_old_files(file_ids=old_file_ids)

get_draftkings_data()

# {
#     "code_interpreter": {
#       "file_ids": [file.id]
#     }
#   }