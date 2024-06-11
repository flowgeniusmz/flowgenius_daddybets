import streamlit as st
import pandas as pd
from openai import OpenAI
import requests
import json
import time
from typing import Literal
import datetime


request_headers = {'Accept': 'application/json','User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36','Accept-Language': 'en-US,en;q=0.9','Accept-Encoding': 'gzip, deflate, br'}
client = OpenAI(api_key = st.secrets.openai.api_key)
assistantid = st.secrets.openai.assistant_id



class DataFileUtilities:
    @staticmethod
    def write_json_to_file(json_data, type: Literal["odds", "events"]):
        if type == "events":
            file_path = st.secrets.data.file_path_events
        elif type == "odds":
            file_path = st.secrets.data.file_path_odds
        with open(file_path, 'w') as file:
            json.dump(json_data, file, indent=4)

    @staticmethod
    def read_json_from_file(type: Literal["odds", "events"]):
        if type == "events":
            file_path = st.secrets.data.file_path_events
        elif type == "odds":
            file_path = st.secrets.data.file_path_odds
        with open(file_path, 'r') as file:
            json_data = json.load(file)
        return json_data

    @staticmethod
    def create_oai_file(type: Literal["odds", "events"]):
        if type == "events":
            file_path = st.secrets.data.file_path_events
        elif type == "odds":
            file_path = st.secrets.data.file_path_odds
        file = open(file=file_path, mode="rb")
        oaifile = client.files.create(file=file, purpose="assistants")
        oaifileid = oaifile.id
        return oaifileid

    @staticmethod
    def delete_oai_file(file_id: str):
        client.files.delete(file_id=file_id)

    @staticmethod
    def add_oai_files_to_assistant(file_ids):
        updatevalue = {"code_interpreter": {"file_ids": file_ids}}
        client.beta.assistants.update(assistant_id=assistantid, tool_resources=updatevalue)

    @staticmethod
    def get_request_json(type: Literal["odds", "events"]):
        if type == "odds":
            url = st.secrets.data.url_odds
        elif type == "events":
            url = st.secrets.data.url_events
        response = requests.get(url=url, headers=request_headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to fetch data from URL: {url} (Status code: {response.status_code})")

    @staticmethod
    def delete_old_files(file_ids):
        for file_id in file_ids:
            client.files.delete(file_id=file_id)

@st.cache_data(ttl=datetime.timedelta(hours=24))
def get_draftkings_data():
    new_file_ids = []
    old_file_ids = client.beta.assistants.retrieve(assistant_id=assistantid).tool_resources.code_interpreter.file_ids

    json_data_odds = DataFileUtilities.get_request_json(type="odds")
    DataFileUtilities.write_json_to_file(json_data=json_data_odds, type="odds")
    odds_file_id = DataFileUtilities.create_oai_file(type="odds")
    new_file_ids.append(odds_file_id)

    json_events_data = DataFileUtilities.get_request_json(type="events")
    DataFileUtilities.write_json_to_file(json_data=json_events_data, type="events")
    events_file_id = DataFileUtilities.create_oai_file(type="events")
    new_file_ids.append(events_file_id)

    DataFileUtilities.add_oai_files_to_assistant(file_ids=new_file_ids)
    DataFileUtilities.delete_old_files(file_ids=old_file_ids)

get_draftkings_data()

# {
#     "code_interpreter": {
#       "file_ids": [file.id]
#     }
#   }


# file_path_odds = st.secrets.data.file_path_events
# file_path_events = st.secrets.data.file_path_odds
# url_odds = st.secrets.data.url_odds
# url_events = st.secrets.data.url_events