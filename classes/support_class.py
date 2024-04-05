import streamlit as st
from config import pagesetup as ps
import requests
from assets.faqs import faqs as f

class Support:
    def __init__(self):
        self.contact_email = "support@daddybetsgpt.com"
        self.user_email = None
        self.help_email_url = st.secrets.urlconfig.helpemail
        self.bug_email_url = st.secrets.urlconfig.bugemail
        self.user_email = None
        self.user_name = None
        self.help_description = None
        self.bug_description = None
        self.email_params = None
        self.faq_prompts = f.faq_prompts_content
        self.faq_app = f.faq_app_content
        self.tab_names = ["Contact Support", "Report a Bug", "Prompt Tips and Tricks", "DaddyBets App FAQs"]
        self.main_support_display()
        
    def send_support_email(self, email, name, description, type):
        self.user_email = email
        self.user_name = name
        self.email_params = {"email": email, "name": name, "description": description}
        if type == "help":
            self.help_description = description
            url = self.help_email_url
        if type == "bug":
            self.bug_description = description
            url = self.bug_email_url
        try:
            response = requests.post(url=url, json=self.email_params)
        except Exception as e:
            self.support_display_message("error")
        else:
            self.support_display_message("success")
    
    def support_display_message(self, type):
        if type == "success":
            st.success(body="Your feedback or issue has been submitted! Please allow 24-48 hours for a response.", icon="✅")
        if type == "error":
            st.error(body="Error: Help email failed to send. Please try again in a few mintues.", icon="⚠️")

    def contact_support_display(self):
        ps.get_gray_header(varText="Contact Support")
        con1 = st.container(border=False)
        with con1:
            scon1 = ps.container_styled2(varKey="helptab1")
            with scon1:
                cols1 = st.columns([1,20,1])
                with cols1[1]:
                    email = st.text_input(label="Email", key="_helpemail")
                    name = st.text_input(label="Name", key="helpname")
                    description = st.text_area(label="Question, Comment, or Concern", key="helpdescription", placeholder="Please enter your comments, questions or concerns here...")
                    submit = st.button(label="Submit", key="helpsubmitbutton")
                    if submit:
                        if name is not None and email is not None and description is not None:
                            self.send_support_email(name=name, email=email, description=description, type="help")
                        else:
                            st.error(body="**Error:** Please complete all the fields in the form and try again", icon="⚠️")
    
    def report_bug_display(self):
        ps.get_gray_header(varText="Report a Bug")
        con2 = st.container(border=False)
        with con2:
            scon2 = ps.container_styled2(varKey="helptab2")
            with scon2:
                cols2 = st.columns([1,20,1])
                with cols2[1]:
                    email = st.text_input(label="Email", key="bugemail")
                    name = st.text_input(label="Name", key="bugname")
                    description = st.text_area(label="Question, Comment, or Concern", key="bugdescription", placeholder="Please enter your comments, questions or concerns here...")
                    submit = st.button(label="Submit", key="bugsubmitbutton")
                    if submit:
                        if name is not None and email is not None and description is not None:
                            self.send_support_email(name=name, email=email, description=description, type="bug")
                        else:
                            st.error(body="**Error:** Please complete all the fields in the form and try again", icon="⚠️")

    def faq_prompts_display(self):
        ps.get_gray_header(varText="Prompt Tips and Tricks")
        con3 = st.container(border=False)
        with con3:
            scon3 = ps.container_styled2(varKey="helptab3")
            with scon3:
                content = self.faq_prompts
                st.markdown(content)
                
    def faq_app_display(self):
        ps.get_gray_header(varText="DaddyBets App FAQs")
        con4 = st.container(border=False)
        with con4:
            scon4 = ps.container_styled2(varKey="helptab4")
            with scon4:
                content1 = self.faq_app
                st.markdown(body=content1)

    def main_support_display(self):
        support_container = st.container(border=False, height=600)
        with support_container:
            tab1, tab2, tab3, tab4 = st.tabs(tabs=self.tab_names)
            with tab1:
                self.contact_support_display()
            with tab2:
                self.report_bug_display()
            with tab3:
                self.faq_prompts_display()
            with tab4:
                self.faq_app_display()