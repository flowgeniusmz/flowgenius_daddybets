import streamlit as st
from config import pagesetup as ps, sessionstates as ss
import pandas as pd
import random
from datetime import datetime, timezone
import time
import uuid 


class ChatHistory():
    def __init__(self):
        self.get_chat_session()
        self.set_initial_messages()
        self.set_initial_log_messages()
        
    
    def get_chat_session(self):
        self.user_session_id = st.session_state.usersession_id
        self.chat_session_id = str(uuid.uuid4())
        self.chat_session_datetime_start = datetime.now()
        self.chat_session_unixtime_start = int(time.mktime(self.chat_session_datetime_start.timetuple()))
        
    def get_initial_message(self):
        random_number = random.randint(a=1, b=3)
        if random_number == 1:
            initial_message = st.secrets.messageconfig.initialmessage1_daddy
        elif random_number == 2:
            initial_message = st.secrets.messageconfig.initialmessage2_daddy
        else:
            initial_message = st.secrets.messageconfig.initialmessage3_daddy
        return initial_message

    def set_initial_messages(self):
        self.initial_message_content = self.get_initial_message()
        self.initial_message_role = "assistant"
        self.initial_message = {"role": self.initial_message_role, "content": self.initial_message_content}
        self.messages = [self.initial_message]
        
    def set_initial_log_messages(self):
        self.initial_message_assistant_id = "0"
        self.initial_message_thread_id = "0"
        self.initial_message_id = "0"
        self.initial_message_run_id = "0"
        self.initial_message_datetime = datetime.now()
        self.initial_message_unixtime = int(time.mktime(self.initial_message_datetime.timetuple()))
        self.initial_log_message = {
            "chat_session_id": self.chat_session_id, 
            "chat_session_datetime_start": self.chat_session_datetime_start, 
            "chat_session_unixtime_start": self.chat_session_unixtime_start, 
            "user_session_id": self.user_session_id, 
            "role": self.initial_message_role, 
            "content": self.initial_message_content, 
            "assistant_id": self.initial_message_assistant_id, 
            "thread_id": self.initial_message_thread_id, 
            "message_id": self.initial_message_id, 
            "run_id": self.initial_message_run_id, 
            "datetime": self.initial_message_datetime, 
            "unixtime": self.initial_message_unixtime
            }
        self.log_messages = [self.initial_log_message]
        
    def get_messages_length(self):
        messages_length = len(self.messages)
        self.messages_length = messages_length
        return messages_length
    
    def get_chat_history_display_type(self, messages_length):
        if messages_length >= 1:
            display_chat_history = True
            display_chat_history_type = "success"
        elif messages_length < 1:
            display_chat_history = False
            display_chat_history_type = "info"
        else:
            display_chat_history = False
            display_chat_history_type = "error"
        self.display_chat_history = display_chat_history
        self.display_chat_history_type = display_chat_history_type
        return display_chat_history, display_chat_history_type
    
    def get_chat_history_display(self):
        messages_length = self.get_messages_length()
        display, display_type = self.get_chat_history_display_type(messages_length=messages_length)
        maincontainer = ps.container_styled2(varKey="maincontainerch")
        with maincontainer:
            if display:
                self.get_chat_history_display_success()
            else:
                if display_type == "info":
                    self.get_chat_history_display_info()
                else:
                    self.get_chat_history_display_error()


    def get_chat_history_display_success(self):
        df_log_messages = pd.DataFrame(self.log_messages)
        df_log_messages_filtered = df_log_messages[df_log_messages['run_id'] != "0"]
        df_log_messages_grouped = df_log_messages_filtered.groupby('run_id')
        for run_id, group in df_log_messages_grouped:
            user_msgs = group[group['role'] == 'user']['content']
            assistant_msgs = group[group['role'] == 'assistant']['content']

            run_container = ps.container_styled3(varKey=f"runcontainer_{run_id}")
            with run_container:
                header_container = st.container(border=False)
                with header_container:
                    runid = st.text_input(label="Run Id", value=run_id, disabled=True)
                body_container = st.container(border=False)
                with body_container:
                    cols = st.columns([10,1,10])
                    with cols[0]:
                        usermessages = st.popover(label="User Messages", use_container_width=True, disabled=False)
                        with usermessages:
                            for msg in user_msgs:
                                st.markdown(msg)
                    with cols[2]:
                        asstmessages = st.popover(label="Assistant Messages", use_container_width=True, disabled=False)
                        with asstmessages:
                            for msg in assistant_msgs:
                                st.markdown(msg)
        
    def get_chat_history_display_error(self):
        warning_container = st.container(border=False)
        with warning_container: 
            warning_message = st.warning(
                body="**ERROR: Chat History Not Displayed:** You must first go to **Manage Assistant** page first before any chat history will be displayed. Please use the link below to go to **Manage Assistant** and then return back to **Chat History**. (Note: This is a temporary bug that will be resolved)",
                icon="⚠️"
            )
            manage_page_link = st.page_link(
                page="pages/2_💬_Betting_Assistant.py",
                label="Click here to go back to **Manage Assistant**",
                icon="💬"
            )
            
    def get_chat_history_display_info(self):
        error_container = st.container(border=False)
        with error_container: 
            error_message = st.error(
                body="**ERROR: No Chat History:** No chat history has been found. Please use the link below to go back to the **Assistant Chat**. Once you start a chat, your chat history will be displayed!",
                icon="⚠️"
            )
            chat_page_link = st.page_link(
                page="pages/2_💬_Betting_Assistant.py",
                label="Click here to go back to **Assistant Chat**",
                icon="💬"
            )

    def add_user_message(self, prompt, messageid, assistantid, threadid, runid):
        self.new_user_message = {"role": "user", "content": prompt}
        self.new_user_log_message = {
            "chat_session_id": self.chat_session_id, 
            "chat_session_datetime_start": self.chat_session_datetime_start, 
            "chat_session_unixtime_start": self.chat_session_unixtime_start, 
            "user_session_id": self.user_session_id, 
            "role": "user", 
            "content": prompt, 
            "assistant_id": assistantid, 
            "thread_id": threadid, 
            "message_id": messageid, 
            "run_id": runid, 
            "datetime": datetime.now(), 
            "unixtime": int(time.mktime(datetime.now().timetuple()))
            }
        self.messages.append(self.new_user_message)
        self.log_messages.append(self.new_user_log_message)

    def add_assistant_message(self, prompt, messageid, assistantid, threadid, runid):
        self.new_user_message = {"role": "assistant", "content": prompt}
        self.new_user_log_message = {
            "chat_session_id": self.chat_session_id, 
            "chat_session_datetime_start": self.chat_session_datetime_start, 
            "chat_session_unixtime_start": self.chat_session_unixtime_start, 
            "user_session_id": self.user_session_id, 
            "role": "assistant", 
            "content": prompt, 
            "assistant_id": assistantid, 
            "thread_id": threadid, 
            "message_id": messageid, 
            "run_id": runid, 
            "datetime": datetime.now(), 
            "unixtime": int(time.mktime(datetime.now().timetuple()))
            }
        self.messages.append(self.new_user_message)
        self.log_messages.append(self.new_user_log_message)