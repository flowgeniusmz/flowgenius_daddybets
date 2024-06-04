import streamlit as st
import requests
import json


eventgroupid = "42133"
sportid = "3"
regionlower = "il"
regionupper = "IL"


def get_formatted_url(varType, varEventGroupId: str=None, varSportId: str=None, varRegionUpper: str=None, varRegionLower: str=None):
    url_odds = "https://sportsbook-nash-us{regionlower}.draftkings.com/sites/US-{regionupper}-SB/api/v5/eventgroups/{eventgroupid}?format=json"
    url_events = "https://sportsbook.draftkings.com/sites/US-{regionupper}-SB/api/sportsdata/v1/sports/{sportid}/events.json"
    url_seasons = "https://sportsbook.draftkings.com/sites/US-{regionupper}-SB/api/sportsdata/v1/sports/{sportid}/seasons.json"
    url_standings = "https://sportsbook.draftkings.com/sites/US-{regionupper}-SB/api/sportsdata/v1/sports/{sportid}/standings.json"
    if varType == "odds": 
        url = url_odds.format(regionlower=varRegionLower, regionupper=varRegionUpper, eventgroupid=varEventGroupId)
    elif varType == "events": 
        url = url_events.format(regionupper=varRegionUpper, sportid=varSportId)
    elif varType == "seasons": 
        url = url_seasons.format(regionupper=varRegionUpper, sportid=varSportId)
    elif varType == "standings": 
        url = url_standings.format(regionupper=varRegionUpper, sportid=varSportId)
    return url

formatted_odds_url = get_formatted_url("odds", eventgroupid, sportid, regionupper, regionlower)
formatted_events_url = get_formatted_url("events", eventgroupid, sportid, regionupper, regionlower)
oddjson = requests.get(url=formatted_odds_url).json()
print(oddjson)
eventjson = requests.get(url=formatted_events_url).json()
print(eventjson)
