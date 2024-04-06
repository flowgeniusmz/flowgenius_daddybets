import streamlit as st
from config import pagesetup as ps
from openai import OpenAI
import time
import json
from tavily import TavilyClient




def tavily_search(query):
    search_results = TavilyClient(api_key=st.secrets.tavily.apikey).get_search_context(query=query, search_depth="advanced", max_tokens=8000)
    return search_results

class BettingAssistant():
    def __init__(self):
        self.client = OpenAI(api_key=st.secrets.openai.apikey)
        self.get_assistant()
        self.get_thread()
        
    def get_assistant(self):
        self.assistant_id = st.secrets.openai.assistantid
        self.assistant = self.client.beta.assistants.retrieve(assistant_id=self.assistant_id)
    
    def get_thread(self):
        self.thread = self.client.beta.threads.create()
        self.thread_id = self.thread.id
        
    def create_message(self, prompt, file_ids=None):
        self.message = self.client.beta.threads.messages.create(thread_id=self.thread_id, role="user", content=prompt, file_ids=file_ids)
        self.message_id = self.message.id
        self.user_message_id = self.message_id
        self.user_message_content = prompt
    
        
    def create_run(self, additional_instructions=None):
        self.run = self.client.beta.threads.runs.create(thread_id=self.thread_id, assistant_id=self.assistant_id, additional_instructions=additional_instructions)
        self.run_id = self.run.id
        self.run_status = self.run.status

    def retrieve_run(self):
        self.run = self.client.beta.threads.runs.retrieve(run_id=self.run_id, thread_id=self.thread_id)
        self.run_status = self.run.status
        
    def wait_on_run(self):
        while self.run_status != "completed":
            time.sleep(1)
            self.retrieve_run()
            if self.run_status == "completed":
                self.get_thread_messages()
                self.get_response_messages()
                break
            elif self.run_status == "requires_action":
                self.tool_calls = self.run.required_action.submit_tool_outputs.tool_calls
                self.requires_action_type = self.run.required_action.type # should be submit_tool_outputs
                self.submit_tool_outputs()
                if self.tool_outputs:
                    self.retrieve_run()
                
    def submit_tool_outputs(self):
        self.tool_outputs = []
        for tool_call in self.tool_calls:
            toolname = tool_call.function.name
            toolargs = json.loads(tool_call.function.arguments)
            toolid = tool_call.id
            if toolname == "tavily_search":
                toolarg = toolargs['query']
                tooloutput = tavily_search(query=toolarg)
                toolcalloutput = {"tool_call_id": toolid, "output": tooloutput}
                self.tool_outputs.append(toolcalloutput)
    
    def get_thread_messages(self):
        self.thread_messages = self.client.beta.threads.messages.list(thread_id=self.thread_id)
    
    def get_response_messages(self):
        for thread_message in self.thread_messages:
            if thread_message.role == "assistant" and thread_message.run_id == self.run_id:
                #response_message = st.session_state.chat_history.add_assistant_message(prompt=thread_message.content[0].text.value, messageid=thread_message.id, assistantid=self.assistant_id, threadid=self.thread_id, runid=self.run_id)          
                self.assistant_message_id = thread_message.id
                self.assistant_message_content = thread_message.content[0].text.value
    
    def add_and_display_message(self, type):
        if type == "user":
            self.add_message_to_chat_history(type="user")
            self.display_message(type="user")
        else:
            self.add_message_to_chat_history(type="assistant")
            self.display_message(type="assistant")
            
    def add_message_to_chat_history(self, type):
        if type == "user":
            st.session_state.chat_history.add_user_message(prompt=self.user_message_content, assistantid = self.assistant_id, threadid = self.thread_id, messageid = self.user_message_id, runid = self.run_id)    
        else:
            st.session_state.chat_history.add_assistant_message(prompt=self.assistant_message_content, assistantid = self.assistant_id, threadid = self.thread_id, messageid = self.assistant_message_id, runid = self.run_id)
            
    def display_message(self, type):
        if type == "user":
            role = "user"
            content = self.user_message_content
        else:
            role = "assistant"
            content = self.assistant_message_content
        with st.chat_message(name=role):
            st.markdown(body=content)
        
    def run_assistant(self, prompt, file_ids=None):
        self.create_message(prompt=prompt, file_ids=file_ids)
        self.create_run()
        self.add_and_display_message(type="user")
        self.wait_on_run()
        self.add_and_display_message(type="assistant")

