import streamlit as st
import stripe
import requests
from supabase import create_client, Client
from config import pagesetup as ps
from userflow import userflow4_usersession as uf4
import re

def valid_username(email):
    # Regular expression for validating an Email
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w{2,3}$'
    if re.match(pattern, email):
        return True
    else:
        return False


def send_welcome_email(username, credential, name):
    url = st.secrets.urlconfig.welcomeemail
    body = {"username": username, "credential": credential, "name": name}
    response = requests.post(url=url, json=body)
    st.toast(body=f"Welcome email successfully sent to {username}!")

def create_stripe_checkout_session(customer_email: str=None):
    session = stripe.checkout.Session.create(
        api_key=st.secrets.stripe.api_key,
        ui_mode=st.secrets.stripe.checkout_ui_mode,
        mode=st.secrets.stripe.checkout_mode,
        line_items=[{"price": st.secrets.stripe.checkout_lineitem_price, "quantity": st.secrets.stripe.checkout_lineitem_quantity}],
        cancel_url=st.secrets.stripe.cancel_url,
        success_url="https://chat.daddybetsgpt.com/return.html?session_id={CHECKOUT_SESSION_ID}" + f"&username={st.session_state.username}&credential={st.session_state.credential}",
        #success_url="https://solid-happiness-qw7w5wwwvr9fw5q-8501.app.github.dev/?session_id={CHECKOUT_SESSION_ID}" + f"&username={st.session_state.username}&credential={st.session_state.credential}",
        
        #success_url="http://localhost:8501/?session_id={CHECKOUT_SESSION_ID}" + f"&username={st.session_state.username}&credential={st.session_state.credential}",
        customer_email=customer_email
        )
    return session

def retrieve_stripe_checkout_session(session_id):
    session = stripe.checkout.Session.retrieve(
        api_key=st.secrets.stripe.api_key,
        id=session_id
    )
    st.session_state.stripe_session = session
    st.session_state.stripe_session_id = session.id
    st.session_state.stripe_customer_email = session.customer_email
    st.session_state.customer_address_state = session.customer_details.address.state
    st.session_state.customer_address_zip = session.customer_details.address.postal_code
    st.session_state.stripe_customer_name = session.customer_details.name
    st.session_state.stripe_payment_status = session.payment_status
    st.session_state.stripe_payment_intent = session.payment_intent
    return session

def callback_newuserform(username, credential):
    checkusername = valid_username(email=username)
    if checkusername:
        Client = create_client(supabase_key=st.secrets.supabase.api_key, supabase_url=st.secrets.supabase.url)
        table = st.secrets.supabase.table_users
        unamecol = st.secrets.supabase.username_col
        credcol = st.secrets.supabase.password_col
        auth_data = {
            unamecol: username,
            credcol: credential
        }
        try:
            data, _ = (Client.table(table_name=table).insert(json=auth_data).execute())
        except Exception as e:
            st.error(body="Unable to create account. Please try again")
        else:
            st.session_state.geolocation_complete = uf4.get_geolocation()
            st.session_state.userflow_complete = True
            st.session_state.checkuser = True
            #st.session_state.userflow_stage = 4
            st.toast(body="Account successfully created!")
            send_welcome_email(username = username, credential = credential, name = st.session_state.stripe_customer_name)
            ps.switch_to_homepage()
    else:
        st.error("**Error**: Invalid username - username must be a valid email address. Please update and try again.")

def callback_payinfo():
    st.session_state.payinfo = True    


def NewUserForm():
    newuserform_container = ps.container_styled2(varKey="newuser") # st.container(border=True)
    with newuserform_container:
        cols = st.columns([1,20,1])
        with cols[1]:
            if st.query_params:
                session=retrieve_stripe_checkout_session(session_id=st.query_params.session_id)
                name = session.customer_details.name
                username = st.text_input(label="Username", value=st.query_params.username, key="_username")

                credential = st.text_input(label="Password", key="_credential", type="password")
                create = st.button(label="Create Account", key="createaccount", on_click=callback_newuserform, args=[username, credential], type="primary")
            else:
                username = st.text_input(label="Username", key="username")
                credential = st.text_input(label="Password", type="password", key="credential")
                payinfo = st.checkbox(label="You will be redirected to Stripe to process your payment. Once completed you will return to DaddyBets. Click here to acknowledge.", key="_payinfo", on_change=callback_payinfo, value=st.session_state.payinfo)
                if payinfo:
                    checkusername = valid_username(email=username)
                    if checkusername:
                        session = create_stripe_checkout_session(customer_email=username)
                        sessionurl = session.url
                        st.link_button(label="Proceed to Checkout", url=sessionurl, type="primary")
                    else:
                        st.error("**Error**: Invalid username - username must be a valid email address. Please update and try again.")
