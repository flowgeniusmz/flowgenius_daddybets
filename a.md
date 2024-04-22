async def get_research(self, user_prompt):
        researchstatus = st.status(label="Performing research...", expanded=False, state="running")
        st.toast(body="Performing research...", icon="⏳")
        research_instance = Research(user_input=user_prompt)
        self.research = await research_instance.get_assistant_research()
        self.format_base_prompt(user_request=user_prompt, research=self.research)
        with researchstatus:
            st.markdown(self.formatted_prompt)
        researchstatus.update(label="Research complete!", expanded=False, state="complete")