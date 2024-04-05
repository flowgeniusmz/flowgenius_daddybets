import streamlit as st
from config import pagesetup as ps


# 0. Set page config
st.set_page_config(page_title=st.secrets.appconfig.app_name, page_icon=st.secrets.appconfig.app_icon, layout=st.secrets.appconfig.app_layout, initial_sidebar_state=st.secrets.appconfig.app_initial_sidebar)
page = 0
ps.master_page_display_styled_popmenu(varPageNumber=page)








