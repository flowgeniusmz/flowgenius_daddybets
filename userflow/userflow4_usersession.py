import streamlit as st
import requests
import uuid
import time
from datetime import datetime



def util_get_uuid():
    get_uuid = str(uuid.uuid4())
    return get_uuid

def util_get_datetime(varType: str):
    datetime_now = datetime.now()
    if varType == "datetime":
        get_datetime = datetime_now
    elif varType == "unixtime":
        get_datetime = int(time.mktime(datetime_now.timetuple()))
    return get_datetime

def get_geolocation():
    url = st.secrets.urlconfig.geolocationurl
    response = requests.get(url=url)
    response_json = response.json()
    location = response_json["location"]
    siteexperience = response_json["siteExperience"]
    isvpn = response_json["isVpn"]
    regionfull = f"{location}-SB"
    region = location.split("US-")[-1]
    regionlower = region.lower()
    geojson = {"location": location, "site_experience": siteexperience, "is_vpn": isvpn, "region_full": regionfull, "region_lower": regionlower}
    
    
    st.session_state.geolocation_response = response_json
    st.session_state.geolocation_json = geojson
    st.session_state.geolocation_location = location
    st.session_state.geolocation_siteexperience = siteexperience
    st.session_state.geolocation_isvpn = isvpn
    st.session_state.geolocation_regionfull = regionfull
    st.session_state.geolocation_region = region
    st.session_state.geolocation_regionlower = regionlower
    
    return True


def create_user_session():
    st.session_state.usersession_id = util_get_uuid()
    st.session_state.usersession_datetime = util_get_datetime(varType="datetime")
    st.session_state.usersession_unixtime = util_get_datetime(varType="unixtime")
    return True
        

