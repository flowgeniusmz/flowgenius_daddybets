import streamlit as st
import uuid
from datetime import datetime
import time
import json
from openai import OpenAI
import pandas as pd
from classes import chathistory_class as clsChatHistory

def initial_session_State():
    if "userflow_complete" not in st.session_state:
        st.session_state.userflow_complete = False
        st.session_state.username = None
        st.session_state.credential = None
        st.session_state.usercheck = False
        st.session_state.payinfo = bool(st.query_params)
        st.session_state.fullname = None
    if "auth_complete" not in st.session_state:
        st.session_state.auth_complete = False
    if "usertype_complete" not in st.session_state:
        st.session_state.usertype_complete = bool(st.query_params)
        st.session_state.usertypes = ["New User Registration", "Existing User Login"]
        st.session_state.selected_usertype = "New User Registration" if st.query_params else None
        st.session_state.usertype = "new" if st.query_params else None
    if "terms_complete" not in st.session_state:
        st.session_state.terms_complete = bool(st.query_params)
        st.session_state.terms_acknowledged = bool(st.query_params)
        st.session_state.terms_accepted = bool(st.query_params)
    if "query_params" not in st.session_state:
        st.session_state.query_params = st.query_params
        st.session_state.query_params_empty = not bool(st.query_params)
    if "stripe_session" not in st.session_state:
        st.session_state.stripe_session = None
        st.session_state.stripe_session_id = st.query_params.get("session_id", None)
        st.session_state.stripe_customer_email = None
        st.session_state.customer_address_state = None
        st.session_state.customer_address_zip = None
        st.session_state.stripe_customer_name = None
        st.session_state.stripe_payment_status = None
        st.session_state.stripe_payment_intent = None
    if "geolocation_complete" not in st.session_state:
        st.session_state.geolocation_complete = False
        st.session_state.geolocation_response = None
        st.session_state.geolocation_json = None
        st.session_state.geolocation_location = None
        st.session_state.geolocation_siteexperience = None
        st.session_state.geolocation_isvpn = None
        st.session_state.geolocation_regionfull = None
        st.session_state.geolocation_region = None
        st.session_state.geolocation_regionlower = None
    if "usersession_complete" not in st.session_state:
        st.session_state.usersession_complete = False
        st.session_state.usersession_id = str(uuid.uuid4())
        st.session_state.usersession_datetime = datetime.now()
        st.session_state.usersession_unixtime =  int(time.mktime(st.session_state.usersession_datetime.timetuple()))
    if "usersession_logged" not in st.session_state:
        st.session_state.usersession_logged = False
    if "userflow_stage" not in st.session_state:
        st.session_state.userflow_stage = 0
    if "client" not in st.session_state:
        st.session_state.client = None
        st.session_state.openai_model = st.secrets.openai.model_gpt4_preview
    #Assistants
    if "assistant" not in st.session_state:
        st.session_state.assistant = None
        st.session_state.assistant_id = None
    #Threads
    if "thread" not in st.session_state:
        st.session_state.thread = None
        st.session_state.thread_id = None  
    #Messages
    if "chatmessages" not in st.session_state:
        st.session_state.chatmessages = [{"role": "assistant", "content": st.secrets.messageconfig.initialmessage3_daddy}]
        st.session_state.prompt = None
        st.session_state.response = None
        st.session_state.promptmessage = {"role": "user", "content": None}
        st.session_state.promptmessages = []
        st.session_state.responsemessage = {"role": "assistant", "content": None}
        st.session_state.responsemessages = []
        st.session_state.threadmessage = None
        st.session_state.threadmessage_id = None
        st.session_state.threadmessage_prompt = None
        st.session_state.threadmessage_response = None
        st.session_state.logmessage = {"assistant_id": st.secrets.openai.assistantid, "thread_id": None, "message_id": None, "role": "assistant", "run_id": None, "content": st.secrets.messageconfig.initialmessage1_daddy, "createddatetime": datetime.now(), "createdunixtime": None}
        st.session_state.logmessages = [{"assistant_id": "0", "thread_id": "0", "message_id": "0", "role": "assistant", "run_id": "0", "content": st.secrets.messageconfig.initialmessage1_daddy, "createddatetime": datetime.now(), "createdunixtime": 0}]
    #Runs
    if "run" not in st.session_state:
        st.session_state.run = {"status": None}
        st.session_state.run_id = None
        st.session_state.run_status = None
        st.session_state.run_instructions = "Ensure you review all your instructions and documents you have been provided. Ensure you follow the process. Ensure you perform your simulations. Ensure you return the types of bets being requested."
    if "openai_client" not in st.session_state:
        st.session_state.openai_client = OpenAI(api_key=st.secrets.openai.api_key)
        st.session_state.openai_model = st.secrets.openai.model_gpt4_preview
    if "start_chat" not in st.session_state:
        st.session_state.start_chat = True
    if "start_manage" not in st.session_state:
        st.session_state.start_manage = False
    if "messages" not in st.session_state:
        st.session_state.initial_message = None
        st.session_state.messages = None
    if "retry_error" not in st.session_state:
        st.session_state.retry_error = 0
    if "data_loaded" not in st.session_state:
        st.session_state.data_loaded=False
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = clsChatHistory.ChatHistory()
    if "initialized" not in st.session_state:
        st.session_state.intialized = True