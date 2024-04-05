import streamlit as st
from config import pagesetup as ps

def callback_usertypeform():
    if st.session_state.selected_usertype is not None:
        st.session_state.usertype_complete = True
        #st.session_state.userflow_stage = 2
        if st.session_state.selected_usertype == "New User Registration":
            st.session_state.usertype = "new"
        else:
            st.session_state.usertype = "existing"
    
    
def UserTypeForm():
    usertypeform_container = ps.container_styled2(varKey="usertype") #st.container(border=True)
    with usertypeform_container:
        select_usertype = st.radio(label="Select New or Existing User", key="selected_usertype", options=st.session_state.usertypes, index=None, on_change=callback_usertypeform, horizontal=True)