import streamlit as st
from config import pagesetup as ps
from classes.assistant_class import BettingAssistant


# 0. Set page config
st.set_page_config(page_title=st.secrets.appconfig.app_name, page_icon=st.secrets.appconfig.app_icon, layout=st.secrets.appconfig.app_layout, initial_sidebar_state=st.secrets.appconfig.app_initial_sidebar)
page = 1
ps.master_page_display_styled_popmenu(varPageNumber=page)


betasst = BettingAssistant()
containera = st.container( border=False)
with containera:
    main_container = ps.container_styled2(varKey="afdfkda")
    with main_container:
        cols = st.columns([20,1,5])
        with cols[0]:
            ps.get_gray_header(varText="Chat with Daddy")
            chat_container_shell = st.container(height=375, border=False)
            with chat_container_shell:
                chat_container = ps.container_styled3(varKey="daf")
                with chat_container:
                    for msg in st.session_state.chat_history.messages:
                        with st.chat_message(msg['role']):
                            st.markdown(msg['content'])
        with cols[2]:
            ps.get_gray_header(varText="Bet Lab")
            status_container = st.container(border=True, height=375)
            with status_container:
                status_placeholder1 = st.empty()
                with status_placeholder1:
                    st.caption(body="Enter a chat to see real-time status.") 
                status_placeholder2 = st.empty()
                with status_placeholder2:
                    st.caption(body="Enter a chat to see real-time status.")  
                status_placeholder3 = st.empty()
                with status_placeholder3:
                    st.caption(body="Enter a chat to see real-time status.")  
footcontainer = st.container()
with footcontainer:
    if prompt := st.chat_input(placeholder="Type here"):
        with chat_container:
            betasst.run_assistant(prompt=prompt)






