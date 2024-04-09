import streamlit as st
from config import pagesetup as ps, sessionstates as ss
from classes.assistant_class import BettingAssistant
from classes.status_class import initialize_status


# 0. Set page config
st.set_page_config(page_title=st.secrets.appconfig.app_name, page_icon=st.secrets.appconfig.app_icon, layout=st.secrets.appconfig.app_layout, initial_sidebar_state=st.secrets.appconfig.app_initial_sidebar)
page = 1
ps.master_page_display_styled_popmenu(varPageNumber=page)

if "chat_history" not in st.session_state:
    ss.initial_session_State()

betasst = BettingAssistant()
containera = st.container( border=False)
with containera:
    main_container = ps.container_styled2A(key="afdfkda", border=False)
    with main_container:
        #cols = st.columns([20,1,5])
        #with cols[0]:
        ps.get_gray_header(varText="Chat with Daddy")
        chat_container = ps.container_styled_3a(key="dafdfdasfsd", border=True, height=400)
        with chat_container:
            for msg in st.session_state.chat_history.messages:
                with st.chat_message(msg['role']):
                    st.markdown(msg['content'])
            #chat_container_shell = st.container(height=375, border=False)
            #with chat_container_shell:
                #chat_container = ps.container_styled3(varKey="daf")
                #with chat_container:
                    #for msg in st.session_state.chat_history.messages:
                        #with st.chat_message(msg['role']):
                            #st.markdown(msg['content'])
            
        #with cols[2]:
        #    ps.get_gray_header(varText="Bet Lab")
        #    status_container = ps.container_styled_3a(key="dafdasfksadfsd", border=True, height=300)
        #    with status_container:
        #        status_placeholder1 = st.empty()
        #        with status_placeholder1:
        #            st.caption("Enter chat to see status")
        #        status_placeholder2 = st.empty()
        #        with status_placeholder2:
        #            st.caption("Enter chat to see status")
            #status_container = st.container(border=True, height=375)
            #with status_container:
                #status_placeholder1 = st.empty()
                #with status_placeholder1:
                    #st.caption(body="Enter a chat to see real-time status.") 
                #status_placeholder2 = st.empty()
                #with status_placeholder2:
                    #st.caption(body="Enter a chat to see real-time status.")  
                #status_placeholder3 = st.empty()
                #with status_placeholder3:
                    #st.caption(body="Enter a chat to see real-time status.")  
betasstprompt = betasst.display_and_get_prompt(chat_container=chat_container)

spacecontainer = st.container(border=False, height=50)













