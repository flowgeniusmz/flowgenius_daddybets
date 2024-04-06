import streamlit as st
from config import pagesetup as ps, sessionstates as ss
import pandas as pd
from classes import chathistory_class as c

# 0. Set page config
st.set_page_config(page_title=st.secrets.appconfig.app_name, page_icon=st.secrets.appconfig.app_icon, layout=st.secrets.appconfig.app_layout, initial_sidebar_state=st.secrets.appconfig.app_initial_sidebar)
page = 2
ps.master_page_display_styled_popmenu(varPageNumber=page)

# 2. Get Chat History
st.session_state.chat_history.get_chat_history_display()



