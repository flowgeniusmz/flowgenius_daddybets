import streamlit as st
from config import pagesetup as ps, sessionstates as ss
from assets.terms import terms_content as terms
from userflow import userflow1_terms as uf1, userflow2_usertype as uf2, userflow3_newuser as uf3n, userflow3_existinguser as uf3e, userflow4_usersession as uf4

# 1. Set Page Config
st.set_page_config(page_title=st.secrets.appconfig.app_name, page_icon=st.secrets.appconfig.app_icon, layout=st.secrets.appconfig.app_layout, initial_sidebar_state=st.secrets.appconfig.app_initial_sidebar)

ps.get_page_styling()

ps.display_background_image()

# 3. Session States
ss.initial_session_State()

# 2. Set Page Title
ps.set_title_manual(varTitle="DaddyBets", varSubtitle="Login / Registration", varDiv=True)


userflow_container = st.container(border=False)
with userflow_container:

# 6. Flow
    if st.session_state.userflow_complete:
        ps.switch_to_homepage()    
    elif not st.session_state.terms_complete:
        ps.get_gray_header(varText="Terms and Conditions")
        uf1.TermsForm()
    elif not st.session_state.usertype_complete:
        ps.get_gray_header(varText="Select New or Existing User")
        uf2.UserTypeForm()
    elif not st.session_state.usercheck:
        if st.session_state.usertype == "new": 
            ps.get_gray_header(varText="New User Registraiton")
            uf3n.NewUserForm()
        else:
            ps.get_gray_header(varText="Existing User Login")
            uf3e.ExistingUserForm()

        