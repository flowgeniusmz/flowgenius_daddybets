import streamlit as st
from assets.terms.terms_content import terms_content
from config import pagesetup as ps

def termsform_callback(acknowledged):
    if acknowledged:
        st.session_state.terms_complete = True
        st.session_state.terms_accepted = True
        #st.session_state.userflow_stage = 1
    else:
        st.session_state.terms_complete = False

def TermsForm():
    terms_container = ps.container_styled2(varKey="terms") #st.container(border=True)
    with terms_container:
        terms_cols = st.columns([1,20,5,10,1])
        with terms_cols[1]:
            acknowledged = st.checkbox(label="I acknowledge the DaddyBets Terms and Conditions.", key="terms_acknowledged", value = st.session_state.terms_acknowledged)
        with terms_cols[3]:
            accepted = st.button(label="Accept Terms and Conditions", key="_terms_accepted", on_click=termsform_callback, args=[acknowledged],  type="primary")
        terms_expander = st.expander(label="View Terms and Conditions", expanded=False)
        with terms_expander:
            st.markdown(terms_content)
            