import streamlit as st
from openai import OpenAI, AsyncOpenAI
import asyncio
import nest_asyncio
import pandas as pd
from tavily import TavilyClient
from classes.research_class import ResearchTopic

### VARIABLES
model = "gpt-3.5-turbo"
sysmessages = {"role": "system", "content": "Summarize the information provided to you by the user the the most optimal way to provide to another AI system or assistant. The focus of each summary should contain any relevant information that may impact sports outcomes or sports betting."}
userprompt = """Query: {query}; Content: {content}; Raw Content: {rawcontent}; URL: {url}; Similarity Score: {score}"""
topic_names = [ResearchTopic.INJURY_REPORT, ResearchTopic.NEWS, ResearchTopic.HEAD_TO_HEAD_STATISTICS, ResearchTopic.FUTURES_AND_PROP_BETS]
user_input = "NBA bulls at pistons 4/11/2024"

### FUNCTIONS
def get_queries(topic_names, user_input):
    queries = [topic.get_query_template() for topic in topic_names]
    formatted_queries = [query.format(user_input) for query in queries]
    return formatted_queries

def tavily_search(query, max_results=3, include_raw_content=True, search_depth="basic"):
    data = TavilyClient(api_key=st.secrets.tavily.api_key).search(query=query, search_depth=search_depth, max_results=max_results, include_raw_content=include_raw_content)
    results = data['results']
    return results

async def perform_searches(queries):
    nest_asyncio.apply()  # Ensure compatibility with Jupyter notebooks or similar environments
    
    async def search_and_append_results(query):
        # Assuming tavily_search returns a list of results
        results = tavily_search(query)
        total_count = len(results)  # Determine the total count from the number of results
        return query, results, total_count  # Return query, results, and total result count

    # Gather futures for concurrent execution
    tasks = [search_and_append_results(query) for query in queries]
    results_with_queries_and_counts = await asyncio.gather(*tasks)
    return results_with_queries_and_counts

def create_research_dataframe(results_list):
    research_list = []
    for query, results, total_count in results_list:
        for result in results:
            research_list.append({
                "query": query,  # Include the query
                "total_count": total_count,  # Include the total result count for the query
                "content": result['content'],
                "url": result['url'],
                "score": result['score'],
                "raw_content": result['raw_content'],
                "user_prompt": userprompt.format(query=query, content=result['content'], rawcontent=result['raw_content'], url=result['url'], score=result['score']),
                "messages": [sysmessages, {"role": "user", "content": userprompt.format(query=query, content=result['content'], rawcontent=result['raw_content'], url=result['url'], score=result['score'])}]
            })
    df_results = pd.DataFrame(research_list)
    return df_results

def get_search_results(topic_names, user_input):
    results_list = []
    queries = get_queries(topic_names=topic_names, user_input=user_input)
    results_list = asyncio.run(perform_searches(queries=queries))
    results_df = create_research_dataframe(results_list=results_list)
    prompts = results_df['user_prompt']
    results_df.to_csv("data1.csv")
    print(results_df)
    return results_df, prompts

def get_summaries(prompts):
    summaries = []
    async def get_summary(prompt):
        #messages = [{"role": "system", "content": "Summarize the content provided. Query is what was searched for, all remaining fields are what was returned. Be brief but comprehensive. The output will be used by another system/AI assistant focused on sports analysis, simulations, and betting."}, {"role": "user", "content": prompt}]
        messages = [sysmessages, {"role": "user", "content": prompt}]
        response = await AsyncOpenAI(api_key=st.secrets.openai.apikey).chat.completions.create(model=model, messages=messages, temperature=0, max_tokens=500)
        summaries.append(response.choices[0].message.content)
    async def prompt_to_summarize(prompts):
        await asyncio.gather(*[get_summary(prompt=prompt) for prompt in prompts])
    asyncio.run(prompt_to_summarize(prompts=prompts))
    return summaries

def get_all_research(usermessage):
    search_results, prompts = get_search_results(topic_names=topic_names, user_input=usermessage)
    summaries = get_summaries(prompts=prompts)
    search_results['summary'] = summaries
    search_results.to_csv("data2.csv")
    search_results['summary'].to_csv("data3.csv")
    print(search_results)
    return summaries



