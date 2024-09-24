import streamlit as st
from openai import OpenAI
import requests
import json
from tavily import TavilyClient
from enum import Enum, auto
from typing import List



class ResearchTopic(Enum):
    INJURY_REPORT = ("Provide the latest injury reports for teams and players.", "{} injury report")
    ROSTERS = ("List the current rosters including any recent changes.", "{} team roster")
    SPREADS = ("What are the current betting spreads for upcoming games?", "{} game betting spreads")
    PLAYER_PROPS = ("Give details on player prop bets available for the next games.", "{} player prop bets")
    MONEYLINE = ("What are the moneyline odds for upcoming games?", "{} moneyline odds")
    PREDICTIONS = ("Provide predictions for the next round of games based on statistical analysis.", "{} game predictions")
    NEWS = ("What is the latest news affecting the games, including team announcements and player interviews?", "{} latest sports news")
    TEAM_PERFORMANCE_TRENDS = ("Analyze trends in team performance, highlighting significant changes.", "{} team performance trends")
    PLAYER_PERFORMANCE_TRENDS = ("Investigate trends in player performance to watch.", "{} player performance trends")
    HEAD_TO_HEAD_STATISTICS = ("Offer historical head-to-head statistics between teams or players.", "{} head to head statistics")
    WEATHER_CONDITIONS = ("For outdoor sports, how might weather conditions affect the game outcomes?", "{} weather impact on games")
    REFEREE_UMPIRE_PROFILES = ("Profiles on referees or umpires, focusing on their game handling tendencies.", "{} referee profiles")
    PUBLIC_BETTING_TRENDS = ("Insights into public betting trends and their implications.", "{} public betting trends")
    SHARP_MONEY_INDICATORS = ("Identify where the professional bettors are placing their bets.", "{} sharp betting indicators")
    IN_GAME_BETTING_OPPORTUNITIES = ("Suggestions for in-game or live betting based on current game dynamics.", "{} live betting opportunities")
    MARKET_COMPARISONS = ("Compare odds and lines across different sportsbooks.", "{} sportsbook odds comparison")
    FUTURES_AND_PROP_BETS = ("Analysis for futures markets and prop bets.", "{} futures and prop bets analysis")
    BANKROLL_MANAGEMENT_TIPS = ("Advice on managing a betting bankroll effectively.", "{} bankroll management tips")
    BETTING_SYSTEM_STRATEGY_REVIEWS = ("Analyze and review various betting systems and strategies.", "{} betting system reviews")
    PSYCHOLOGICAL_ASPECTS_OF_BETTING = ("Address psychological challenges associated with betting.", "{} betting psychology tips")
    FANTASY_SPORTS_INSIGHTS = ("Analysis relevant to fantasy sports player selections.", "{} fantasy sports insights")
    INTERNATIONAL_SPORTS_COVERAGE = ("Insights on international sports and leagues.", "{} international sports coverage")

    def __init__(self, description, query_template):
        self.description = description
        self.query_template = query_template

class Research:
    def __init__(self, user_input):
        self.client = OpenAI(api_key=st.secrets.openai.apikey)
        self.tavclient = TavilyClient(api_key=st.secrets.tavily.api_key)
        self.queries1 = {}
        self.results = []
        self.queries = []
        self.topic_names = [ResearchTopic.INJURY_REPORT, ResearchTopic.NEWS, ResearchTopic.HEAD_TO_HEAD_STATISTICS, ResearchTopic.TEAM_PERFORMANCE_TRENDS, ResearchTopic.SPREADS, ResearchTopic.PREDICTIONS]
        self.model = "gpt-4o-mini"
        self.research = []
        self.summaries = []
        self.user_input = user_input

    def get_assistant_research(self):
        self.generate_research()
        return self.summaries
    
    def generate_research(self):
        for topic in self.topic_names:
            query = topic.query_template.format(self.user_input)
            results = self.run_search(query=query)
            summaries = self. summarize_results(search_results=results)
            topic_research = {"queries": query, "results": results, "summaries": summaries}
            topic_summaries = {"topic_name": topic.name, "summaries": summaries}
            self.research.append(topic_research)
            self.summaries.append(topic_summaries)
            
            
    def run_search(self, query, max_results: int=5, search_depth: str="basic", include_raw_content: bool=True):
        data = self.tavclient.search(query=query, search_depth=search_depth, include_raw_content=True, max_results=max_results)
        results = data['results']
        answer = data['answer']
        return results
    
    def summarize_results(self, search_results):
        summaries = []
        for search_result in search_results:
            summary = self.run_completion(search_result=search_result)
            summaries.append(summary)
        return summaries
    
    def run_completion(self, search_result):
        messages = [{"role": "system","content": "Summarize the information provided to you by the user the the most optimal way to provide to another AI system or assistant. The focus of each summary should contain any relevant information that may impact sports outcomes or sports betting."}, {"role": "user", "content": f"{search_result}"}]
        response = self.client.chat.completions.create(model=self.model, messages=messages, temperature=0, max_tokens=500)
        content = response.choices[0].message.content
        return content
    
    def generate_queries(self):
        """Generate queries for each research topic based on user input."""
        for topic in self.topic_names:
            # Format the query template with the user input
            query = topic.query_template.format(self.user_input)
            # Store the generated query in a dictionary with the topic name as the key
            self.queries1[topic.name] = query
            self.queries.append(query)
        
    def get_queries1(self):
        """Print the generated queries for all research topics."""
        for topic, query in self.queries1.items():
            print(f"{topic}: {query}")

#Example Usage:

#user_input = "NBA"  # Example user input
#research = Research(user_input=user_input)
#a = research.generate_research()
#print(a)


### OLD
#def get_summary(search_result):
#    messages = [{"role": "system","content": "Summarize the information provided to you by the user the the most optimal way to provide to another AI system or assistant. The focus of each summary should contain any relevant information that may impact sports outcomes or sports betting."}]
#    new_message = {"role": "user", "content": f"{search_result}"}
#    messages.append(new_message)
#    response = client.chat.completions.create(model=gpt_model, messages=messages, temperature=0, max_tokens=500)
#    content = response.choices[0].message.content
#    return content

#def tavily_search(query):
#    searchresults = tavclient.search(query=query, search_depth="basic", include_raw_content=True, max_results=10)
#    print(searchresults)
#    return searchresults

#def run_summarizer(query):
#    summaries = []
#    data = tavily_search(query=query)
#    results = data['results']
#    for result in results:
#        result_summary = get_summary(search_result=result)
#        summaries.append(result_summary)
#    return summaries

#query = "NBA mavericks at hornets 4/9/2024"
#qsumm = run_summarizer(query=query)
#print(qsumm)