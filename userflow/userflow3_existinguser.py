import streamlit as st
from supabase import create_client, Client
from userflow import userflow4_usersession as uf4
from config import pagesetup as ps
import re

def valid_username(email):
    # Regular expression for validating an Email
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w{2,3}$'
    if re.match(pattern, email):
        return True
    else:
        return False


def callback_existinguserform(username, credential):
    checkusername = valid_username(email=username)
    if checkusername:
        Client = create_client(supabase_key=st.secrets.supabase.api_key, supabase_url=st.secrets.supabase.url)
        table = st.secrets.supabase.table_users
        unamecol = st.secrets.supabase.username_col
        credcol = st.secrets.supabase.password_col
        select_string = f"{unamecol}, {credcol}"
        data, _ = (Client.table(table_name=table).select(select_string).eq(column=unamecol, value=username).eq(column=credcol, value=credential).execute())
        lengthdata = len(data[-1])
        if lengthdata >0:
            st.session_state.geolocation_complete = uf4.get_geolocation()
            st.session_state.usersession_complete = True
            st.session_state.userflow_complete = True
            st.session_state.checkuser = True
            #st.session_state.userflow_stage = 4
            ps.switch_to_homepage()
    else:
        st.error("**Error**: Invalid username - please use a proper email address for your username.")
    

    
    

def ExistingUserForm():
    existinguserform_container = ps.container_styled2(varKey="existinguser") #st.container(border=True)
    with existinguserform_container:
        cols = st.columns([1,20,1])
        with cols[1]:
            username = st.text_input(label="Username", key="username")
            credential = st.text_input(label="Password", key="credential", type="password")
            login = st.button(label="Login", key="login", on_click=callback_existinguserform, args=[username, credential], type="primary")