import streamlit as st
from openai import OpenAI
import time
import json
from tavily import TavilyClient
from classes.status_class import initialize_status
from classes.research_class import Research



def tavily_search(query):
    search_results = TavilyClient(api_key=st.secrets.tavily.apikey).get_search_context(query=query, search_depth="advanced", max_tokens=8000)
    return search_results

class BettingAssistant():
    def __init__(self):
        self.client = OpenAI(api_key=st.secrets.openai.apikey)
        self.get_assistant()
        self.get_thread()
        self.set_completion_attributes()
        self.set_base_prompt()
    
    def get_assistant(self):
        self.assistant_id = st.secrets.openai.assistantid
        self.assistant = self.client.beta.assistants.retrieve(assistant_id=self.assistant_id)
    
    def get_thread(self):
        self.thread = self.client.beta.threads.create()
        self.thread_id = self.thread.id
        
    def create_message(self, prompt, file_ids=None):
        self.user_message_content = prompt
        #self.add_and_display_message(type="user")
        self.display_message(type="user")
        self.get_research(user_prompt=prompt)
        #self.format_base_prompt(user_request=prompt, research=self.research)
        self.message = self.client.beta.threads.messages.create(thread_id=self.thread_id, role="user", content=self.formatted_prompt, file_ids=file_ids)
        self.message_id = self.message.id
        self.user_message_id = self.message_id
        #self.add_message_to_chat_history(type="user")
        #self.user_message_content = prompt
        #self.add_and_display_message(type="user")
        
    def create_run(self, additional_instructions=None):
        self.run = self.client.beta.threads.runs.create(thread_id=self.thread_id, assistant_id=self.assistant_id, additional_instructions=additional_instructions)
        self.run_id = self.run.id
        self.run_status = self.run.status
        self.add_message_to_chat_history(type="user")

    def retrieve_run(self):
        self.run = self.client.beta.threads.runs.retrieve(run_id=self.run_id, thread_id=self.thread_id)
        self.run_status = self.run.status
        
    def wait_on_run(self):
        simulatedstatus = st.status(label="Simulating...", expanded=False, state="running")
        st.toast("Simulating...", icon="⏳")
        while self.run_status != "completed":
            simulatedstatus.update(label="Simulating", expanded=False, state="running")
            st.toast("Simulating...", icon="⏳")
            #with simulatedstatus:
                #st.markdown("Simulating...please wait")
            time.sleep(3)
            self.retrieve_run()
            if self.run_status == "completed":
                self.get_thread_messages()
                self.get_response_messages()
                simulatedstatus.update(label="Simulation complete!", expanded=False, state="complete")
                st.toast("Simulations complete!", icon="✅")
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

    def display_and_get_prompt(self, chat_container):
        prompt_container = st.container(border=False, height=200)
        with prompt_container:
            self.prompt = st.chat_input(placeholder="Ask Daddy here and watch him cook...", key="_BettingAssistantPrompt")
            if self.prompt:
                with chat_container:
                    self.run_assistant(prompt=self.prompt)

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
        #self.get_research(user_prompt=prompt)
        #self.format_base_prompt(user_request=prompt, research=self.research)
        self.create_message(prompt=prompt, file_ids=file_ids)
        self.create_run()
        #self.add_and_display_message(type="user")
        self.wait_on_run()
        self.add_and_display_message(type="assistant")

    def set_completion_attributes(self):
        self.completion_model = "gpt-3.5-turbo"
        self.completion_temp = 0
        self.completion_json_response_format = {"type": "json_object"}
        self.max_tokens = 1000
        self.completion_base_messages_queries = [ {"role": "system", "content": "You are a expert sports and sportsbook researcher. You will be given a user request. You will respond with the best, most effective query strings to research the user request. Your output will be a JSON object. This JSON object will contain 5 arrays. Each array will contain query strings for a specific topic. The topics are as follows:\n1. News: Query strings to find the latest news articles\n2. Roster: Query strings to get the latest roster, active roster, and injury report(s)\n3. Predictions: Query strings to find predictions on the game or games outcome\n4. Odds: Query strings to find the odds for prop, moneyline, and other types of betting odds by major sportsbooks. All should include at least one query to search DraftKings odds\n5. Historical Matchups: Query strings to find historical related matchups and data\n\n### IMPORTANT ###\n- You will always return a minimum of 25 query strings (5 per topic)\n- To ensure you meet this minimum - before you respond you will count the number of query strings that you have created and add more if it is less than 25\n- Your response will be used by other systems; you are only to respond with the JSON object\n\n### JSON OUTPUT TEMPLATE ###\n{\"news\": [\"query string1\", \"query string2\", \"query string3\", \"query string4\", \"\"query string5\"], \"roster\": [\"query string1\", \"query string2\", \"query string3\", \"query string4\", \"\"query string5\"], \"predictions\": [\"query string1\", \"query string2\", \"query string3\", \"query string4\", \"\"query string5\"], \"odds\": [\"query string1\", \"query string2\", \"query string3\", \"query string4\", \"\"query string5\"], \"historical\": [\"query string1\", \"query string2\", \"query string3\", \"query string4\", \"\"query string5\"]}"}, {"role": "user", "content": "Hook me up wit a 3 leg parlay, a player prop and a moneyline bet for the NBA games tonight"}, {"role": "assistant", "content": "{\"news\": [\"NBA announces schedule for tonight's games with key matchups.\", \"Experts highlight potential for high-scoring NBA games tonight.\", \"Injury reports released, affecting tonight's NBA game odds.\", \"NBA fans excited for the clash between top Eastern and Western conference teams.\",\n    \"Sports analysts predict tonight's NBA games to have significant playoff implications.\"], \"roster\": [  \"LeBron James expected to lead the Lakers in tonight's crucial game.\",  \"Celtics' Jayson Tatum in top form ahead of tonight's game.\", \"Rookie sensations to watch in tonight's NBA games.\", \"Key players returning from injury in tonight's matchups.\", \"NBA coaches to deploy new strategies in tonight's games.\"],\n  \"predictions\": [\"Prediction: High-scoring affair between Lakers and Celtics.\", \"Analysts foresee a triple-double performance in tonight's games.\", \"Defensive strategies predicted to dominate in Heat vs. Bucks.\", \"Close outcomes expected in tonight's NBA matchups.\", \"Unexpected underdog victories anticipated in tonight's games.\"], \"odds\": [\"Lakers favored to win against Celtics with a spread of -4.5.\", \"Over/Under set at 210.5 points for the Lakers vs. Celtics game.\", \"Player prop: LeBron James over/under 28.5 points.\", \"Moneyline bet: Golden State Warriors at +130 against the Suns.\", \"3 leg parlay: Lakers to win, LeBron to score 30+, total points over 200.\"], \"historical\": [\"Historical matchup data favors Lakers in games against Celtics.\", \"Last five NBA seasons show increase in average points per game.\", \"Head-to-head, Warriors have 60% win rate against Suns in past seasons.\", \"Memorable triple-double performances in NBA history.\", \"Top 5 upsets in NBA playoff history.\"]}"}]
        self.completion_base_messages_sportobject = [{"role": "system","content": "You are a data analyst. You will identify the sport being discussed in the users prompt / request. You will return the appropriate json object based on the identified sport.\n\n### Sport Objects ###\nNFL: {\"eventGroupId\":\"88808\",\"sportId\":1,\"name\":\"NFL\",\"latestSeasonId\":678,\"latestSeasonYear\":2024,\"latestStartedSeasonId\":652,\"latestStartedSeasonYear\":2023,\"generalSportName\":\"Football\",\"fullName\":\"National Football League\"},\nMLB: {\"eventGroupId\":\"84240\",\"sportId\":2,\"name\":\"MLB\",\"latestSeasonId\":654,\"latestSeasonYear\":2024,\"latestStartedSeasonId\":654,\"latestStartedSeasonYear\":2024,\"generalSportName\":\"Baseball\",\"fullName\":\"Major League Baseball\"},\nNHL: {\"eventGroupId\":\"42133\",\"sportId\":3,\"name\":\"NHL\",\"latestSeasonId\":635,\"latestSeasonYear\":2023,\"latestStartedSeasonId\":635,\"latestStartedSeasonYear\":2023,\"generalSportName\":\"Hockey\",\"fullName\":\"National Hockey League\"}\nNBA: {\"eventGroupId\":\"42648\",\"sportId\":4,\"name\":\"NBA\",\"latestSeasonId\":633,\"latestSeasonYear\":2023,\"latestStartedSeasonId\":633,\"latestStartedSeasonYear\":2023,\"generalSportName\":\"Basketball\",\"fullName\":\"National Basketball Association\"}\nCollege Football: {\"eventGroupId\":\"87637\",\"sportId\":5,\"name\":\"CFB\",\"latestSeasonId\":588,\"latestSeasonYear\":2023,\"latestStartedSeasonId\":588,\"latestStartedSeasonYear\":2023,\"generalSportName\":\"Football\",\"fullName\":\"College Football\"}\nCollege Basketball: {\"eventGroupId\":\"92483\",\"sportId\":6,\"name\":\"CBB\",\"latestSeasonId\":675,\"latestSeasonYear\":2023,\"latestStartedSeasonId\":675,\"latestStartedSeasonYear\":2023,\"generalSportName\":\"Basketball\",\"fullName\":\"Men's College Basketball\"}\nGolf: {\"eventGroupId\":\"92694\",\"sportId\":7,\"name\":\"PGA\",\"latestSeasonId\":645,\"latestSeasonYear\":2023,\"latestStartedSeasonId\":645,\"latestStartedSeasonYear\":2023,\"generalSportName\":\"Golf\",\"fullName\":\"Professional Golfer's Association\"}\nSoccer: {\"sportId\":8,\"name\":\"SOCC\",\"generalSportName\":\"Soccer\",\"fullName\":\"Soccer\"}\nUltimate Fighting: {\"eventGroupId\":\"9034\",\"sportId\":25,\"name\":\"UFC\",\"latestSeasonId\":685,\"latestSeasonYear\":2024,\"latestStartedSeasonId\":674,\"latestStartedSeasonYear\":2024,\"generalSportName\":\"MMA\",\"fullName\":\"Ultimate Fighting Championship\"}"},{"role": "user","content": "Get me bets for the Wizards Magic Game tonight"},{"role": "assistant","content": "{\"eventGroupId\":\"42648\",\"sportId\":4,\"name\":\"NBA\",\"latestSeasonId\":633,\"latestSeasonYear\":2023,\"latestStartedSeasonId\":633,\"latestStartedSeasonYear\":2023,\"generalSportName\":\"Basketball\",\"fullName\":\"National Basketball Association\"}"},{"role": "user","content": "What is the bets for the final four games this weekend? "},{"role": "assistant","content": "{\"eventGroupId\":\"92483\",\"sportId\":6,\"name\":\"CBB\",\"latestSeasonId\":675,\"latestSeasonYear\":2023,\"latestStartedSeasonId\":675,\"latestStartedSeasonYear\":2023,\"generalSportName\":\"Basketball\",\"fullName\":\"Men's College Basketball\"}"},{"role": "user","content": "Yo dawg hook me up with some bets for the chiefs raiders game"},{"role": "assistant","content": "{\"eventGroupId\":\"88808\",\"sportId\":1,\"name\":\"NFL\",\"latestSeasonId\":678,\"latestSeasonYear\":2024,\"latestStartedSeasonId\":652,\"latestStartedSeasonYear\":2023,\"generalSportName\":\"Football\",\"fullName\":\"National Football League\"}"},{"role": "user","content": "let me get that tcu sugarbowl bets"},{"role": "assistant","content": "{\"eventGroupId\":\"87637\",\"sportId\":5,\"name\":\"CFB\",\"latestSeasonId\":588,\"latestSeasonYear\":2023,\"latestStartedSeasonId\":588,\"latestStartedSeasonYear\":2023,\"generalSportName\":\"Football\",\"fullName\":\"College Football\"}"},]
        self.completion_base_messages_teamsobject = [{"role": "system","content": "You are a data analyst and sport expert. Your job is to identify any sports teams being referenced in a users input. You will then return a json object with the following information: \n\n{teams: \"team1\": {\"shortCode\": \"Team's abbreviated code (e.g., 'BOS' for Boston Celtics)\", \"market\": \"The team's city or market (e.g., 'Boston')\", \"marketAbbr\": \"The abbreviated form of the team's market (e.g., 'BOS')\", \"name\": \"The official name of the team (e.g., 'Celtics')\", \"nameShort\": \"The short name of the team, typically the same as the official name (e.g., 'Celtics')\", \"fullname\": \"The full name of the team including the city/market (e.g., 'Boston Celtics')\"}}\n\n"},{"role": "user","content": "Hey, can you snag the latest spread for the Celts game tonight? Hoping Boston's defense locks in."},{"role": "assistant","content": "{\"shortCode\": \"BOS\", \"market\": \"Boston\", \"marketAbbr\": \"BOS\", \"name\": \"Celtics\", \"nameShort\": \"Celtics\", \"fullname\": \"Boston Celtics\"}"},{"role": "user","content": "What's the over/under on the Giants game this Sunday? I got a hunch NY's gonna put up some numbers!"},{"role": "assistant","content": "{ \"shortCode\": \"NYG\",  \"market\": \"New York\",  \"marketAbbr\": \"NY\", \"name\": \"Giants\",  \"nameShort\": \"Giants\", \"fullname\": \"New York Giants\"}"},{"role": "user","content": "Could you check the odds for Duke's matchup in the NCAA tourney? Need to know if the Blue Devils are favored."},{"role": "assistant","content": " {\n  \"shortCode\": \"DUKE\",   \"market\": \"Durham\", \"marketAbbr\": \"DUKE\", \"name\": \"Blue Devils\", \"nameShort\": \"Blue Devils\", \"fullname\": \"Duke Blue Devils\" }"},{"role": "user","content": "I’m looking to place a bet on the next Bama game. Who’s got the better line, the Crimson Tide or their rivals?"},{"role": "assistant","content": "{\"shortCode\": \"BAMA\", \"market\": \"Alabama\", \"marketAbbr\": \"AL\", \"name\": \"Crimson Tide\", \"nameShort\": \"Crimson Tide\", \"fullname\": \"Alabama Crimson Tide\"}"},{"role": "user","content": "Yankees playing tonight? What are the chances Judge hits another homer? Look up the props for me, will ya?"},{"role": "assistant","content": "{\"shortCode\": \"NYY\", \"market\": \"New York\", \"marketAbbr\": \"NY\", \"name\": \"Yankees\", \"nameShort\": \"Yankees\", \"fullname\": \"New York Yankees\"}"},{"role": "user","content": "For my fantasy league, I need the Maple Leafs’ goalie stats and tonight's puck line. Can you dig that up?"},{"role": "assistant","content": "{\"shortCode\": \"TOR\", \"market\": \"Toronto\", \"marketAbbr\": \"TOR\", \"name\": \"Maple Leafs\", \"nameShort\": \"Maple Leafs\", \"fullname\": \"Toronto Maple Leafs\"}"},{"role": "user","content": "Get me bets for the final four matchup between purdue and ncstate"},{"role": "assistant","content": "{\"teams\": {\"team1\": {\"shortCode\": \"NCST\", \"market\": \"North Carolina State\", \"marketAbbr\": \"NCST\", \"name\": \"Wolfpack\", \"nameShort\": \"Wolfpack\", \"fullname\": \"North Carolina State Wolfpack\"}, \"team2\": {\"shortCode\": \"PUR\", \"market\": \"Purdue\", \"marketAbbr\": \"PUR\", \"name\": \"Boilermakers\", \"nameShort\": \"Boilermakers\", \"fullname\": \"Purdue Boilermakers\"}}}"}]

    def get_completion_messages(self, type, prompt):
        new_message = {"role": "user", "content": prompt}
        if type == "queries":
            base_messages = self.completion_base_messages_queries
        elif type == "sportobject":
            base_messages = self.completion_base_messages_sportobject
        elif type == "teamobject":
            base_messages = self.completion_base_messages_teamsobject
        base_messages.append(new_message)
        return base_messages

    def get_completion(self, prompt, completion_type, json_response=False):
        self.completion_messages = []
        self.completion_messages = self.get_completion_messages(type=completion_type, prompt=prompt)
        if json_response:
            response = self.client.chat.completions.create(model=self.completion_model, messages=self.completion_messages, temperature=self.completion_temp, response_format=self.completion_json_response_format, max_tokens=self.max_tokens)        
        else:
            response = self.client.chat.completions.create(model=self.completion_model, messages=self.completion_messages, temperature=self.completion_temp, max_tokens=self.max_tokens)
        response_content = response.choices[0].message.content
        return response_content

    def initialize_statuses(self):
        self.research_status = initialize_status(varType="research")
        self.simulation_status = initialize_status(varType="simulations")
        self.query_status = initialize_status(varType="queries")

    def get_all_completions(self, prompt):
        self.completion_response_teamobject = self.get_completion(prompt=prompt, completion_type="teamobject", json_response=True)
        print(self.completion_response_teamobject)
        self.completion_response_sportsobject = self.get_completion(prompt=prompt, completion_type="sportobject", json_response=True)
        print(self.completion_response_sportsobject)
        self.completion_response_queries = self.get_completion(prompt=prompt, completion_type="queries", json_response=True)
        print(self.completion_response_queries)
        self.completion_response_prompt_base = """Sport Object: {sportobject}
        Team Object: {teamobject}
        Queries: {queries}"""
        self.completion_response_prompt = self.completion_response_prompt_base.format(sportobject = self.completion_response_sportsobject, teamobject = self.completion_response_teamobject, queries = self.completion_response_queries)

    def get_research(self, user_prompt):
        researchstatus = st.status(label="Performing research...", expanded=False, state="running")
        st.toast(body="Performing research...", icon="⏳")
        self.research = Research(user_input=user_prompt).get_assistant_research()
        self.format_base_prompt(user_request=user_prompt, research=self.research)
        with researchstatus:
            st.markdown(self.formatted_prompt)
        researchstatus.update(label="Research complete!", expanded=False, state="complete")
        

    def set_base_prompt(self):
        self.base_prompt = """Its time to shine, Daddy! The user's request and corresponding research are provided below. Ensure you respond directly to the user.
        User Request: {user_request}
        Research: {research}"""
    
    def format_base_prompt(self, user_request, research):
        self.formatted_prompt = self.base_prompt.format(user_request=user_request, research=research)
