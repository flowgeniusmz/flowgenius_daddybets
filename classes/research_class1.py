import asyncio
import nest_asyncio
import pandas as pd
from tavily import TavilyClient
from openai import OpenAI, AsyncOpenAI
import streamlit as st
from enum import Enum


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
        self.user_input = user_input
        self.tavily_api_key = st.secrets["tavily"]["api_key"]
        self.openai_api_key = st.secrets["openai"]["api_key"]
        self.model = "gpt-3.5-turbo"
        self.system_message = {"role": "system", "content": "Summarize the information provided to you by the user the most optimal way to provide to another AI system or assistant. The focus of each summary should contain any relevant information that may impact sports outcomes or sports betting."}
        self.topic_names = [ResearchTopic.INJURY_REPORT, ResearchTopic.NEWS, ResearchTopic.HEAD_TO_HEAD_STATISTICS, ResearchTopic.TEAM_PERFORMANCE_TRENDS, ResearchTopic.SPREADS, ResearchTopic.PREDICTIONS]

    def get_queries(self):
        queries = [topic.value[1] for topic in self.topic_names]  # Adjusted to access tuple correctly
        formatted_queries = [query.format(self.user_input) for query in queries]
        return formatted_queries

    def tavily_search(self, query, max_results=3, include_raw_content=True, search_depth="basic"):
        client = TavilyClient(api_key=self.tavily_api_key)
        data = client.search(query=query, search_depth=search_depth, max_results=max_results, include_raw_content=include_raw_content)
        return data['results']

    async def perform_searches(self, queries):
        nest_asyncio.apply()

        async def search_and_append_results(query):
            results = self.tavily_search(query)
            total_count = len(results)
            return query, results, total_count

        tasks = [search_and_append_results(query) for query in queries]
        results_with_queries_and_counts = await asyncio.gather(*tasks)
        return results_with_queries_and_counts

    async def summarize_content(self, content):
        messages = [self.system_message, {"role": "user", "content": content}]
        async with AsyncOpenAI(api_key=self.openai_api_key) as client:
            response = await client.chat.completions.create(model=self.model, messages=messages, temperature=0, max_tokens=150)
        return response.choices[0].message.content

    async def get_summaries(self, data_frame):
        summaries = await asyncio.gather(*[self.summarize_content(row['content']) for _, row in data_frame.iterrows()])
        data_frame['summary'] = summaries
        return data_frame

    async def get_assistant_research(self):
        queries = self.get_queries()
        results_list = await self.perform_searches(queries)
        df_results = self.create_research_dataframe(results_list)
        df_results_with_summaries = await self.get_summaries(df_results)
        print(df_results_with_summaries)
        return df_results_with_summaries

    def create_research_dataframe(self, results_list):
        research_list = []
        for query, results, total_count in results_list:
            for result in results:
                research_list.append({
                    "query": query,
                    "total_count": total_count,
                    "content": result['content'],
                    "url": result['url'],
                    "score": result['score'],
                    "raw_content": result['raw_content']
                })
        return pd.DataFrame(research_list)
