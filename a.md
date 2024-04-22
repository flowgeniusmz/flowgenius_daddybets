async def get_research(self, user_prompt):
        researchstatus = st.status(label="Performing research...", expanded=False, state="running")
        st.toast(body="Performing research...", icon="⏳")
        research_instance = Research(user_input=user_prompt)
        self.research = await research_instance.get_assistant_research()
        self.format_base_prompt(user_request=user_prompt, research=self.research)
        with researchstatus:
            st.markdown(self.formatted_prompt)
        researchstatus.update(label="Research complete!", expanded=False, state="complete")



          
    async def get_research(self, user_prompt):
        researchstatus = st.status(label="Performing research...", expanded=False, state="running")
        st.toast(body="Performing research...", icon="⏳")
        research_instance = Research(user_input=user_prompt)
        df_results_with_summaries = await research_instance.get_assistant_research()
        research_text = self.format_research_summary(df_results_with_summaries)
        self.format_base_prompt(user_request=user_prompt, research=research_text)
        with researchstatus:
            st.markdown(self.formatted_prompt)
        researchstatus.update(label="Research complete!", expanded=False, state="complete")
    
    def format_research_summary(self, df_results):
        # Convert DataFrame to a single string summary, ensuring full information is passed
        summary_text = "\n".join(f"{idx}. {row['summary']}" for idx, row in df_results.iterrows())
        return summary_text
        

    def set_base_prompt(self):
        self.base_prompt = """Its time to shine, Daddy! The user's request and corresponding research are provided below. Ensure you respond directly to the user.
        User Request: {user_request}
        Research: {research}"""
    
    def format_base_prompt(self, user_request, research):
        self.formatted_prompt = self.base_prompt.format(user_request=user_request, research=research)