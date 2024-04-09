import streamlit as st

class StatusLabel:
    def __init__(self, running, error, complete):
        self.running = running
        self.error = error
        self.complete = complete



class Status:
    def __init__(self, status_labels):
        self.status_labels = status_labels
        self.state = 'initial'  # Initial state
        self.status_object = None

    def create_status(self, label):
        if self.status_object is not None:
            self.status_object.empty()  # Clear previous content
        self.status_object = st.empty()
        self.status_object.status(label)

    def show_toast(self, message, state):
        # Determine the icon based on the state
        if state == 'running':
            icon = "⏳"
        elif state == 'error':
            icon = "⚠️"
        elif state == 'complete':
            icon = "✅"
        else:
            icon = "ℹ️"  # Default info icon
        st.toast(message, icon=icon)

    def start(self):
        self.state = 'running'
        label = self.status_labels.running
        self.create_status(label)
        self.show_toast(label, self.state)

    def write(self, content):
        if self.status_object is not None:
            self.status_object.markdown(content)

    def error(self):
        self.state = 'error'
        label = self.status_labels.error
        self.create_status(label)
        self.show_toast(label, self.state)

    def complete(self):
        self.state = 'complete'
        label = self.status_labels.complete
        self.create_status(label)
        self.show_toast(label, self.state)


research_labels = StatusLabel(
    running="⏳ *DADDY'S BUSY*: Digging deep for those winners",
    error="⚠️ *WHOOPSIE DAISY*: Daddy hit a snag - give it another whirl, sport",
    complete="✅ *BOOM, BABY*: Daddy's got the goods. Let's make some moolah!"
)

simulation_labels= StatusLabel(
    running="🔍 DADDY'S ON THE HUNT: Cracking the numbers, kiddo",
    error="💥 OOF! DADDY'S STUMPED: Might've taken a wrong turn, ace. Try again?",
    complete="🏆 SCORE! DADDY NAILED IT: Grab your notepad, sport - it's winning time."
)

query_labels = StatusLabel(
    running="🔍 BIG DADDY'S ON THE HUNT: Scouring the earth for those golden picks",
    error="💥 OOF! DADDY'S IN A PICKLE: Something went sideways - try tossing the ball again",
    complete="🎯 DADDY STRIKES AGAIN: Grab your gear, it's time to cash in!"
)

weather_labels = StatusLabel(
    running="⏳ **RUNNING**: Getting the latest forecast - please wait...",
    error="⚠️ **ERROR**: Unable to get weather - please try again",
    complete="✅ **COMPLETE**: Odds calculated successfully!"
)
    
odds_labels = StatusLabel(
    running="⏳ **RUNNING**: Crunching numbers hold tight...",
    error="⚠️ **ERROR**: Unable calculating odds - please try again.",
    complete="✅ **COMPLETE**: Odds calculated successfully!"
)

unknown_labels = StatusLabel(
    running="⚠️ **ERROR**: Unknown process",
    error="⚠️ **ERROR**: Unknown process",
    complete="⚠️ **ERROR**: Unknown process"
)

def initialize_status(varType):
    if varType == "research":
        status_instance = Status(research_labels)
    elif varType == "simulations":
        status_instance = Status(simulation_labels)
    elif varType == "queries":
        status_instance = Status(query_labels)
    else:
        status_instance = Status(unknown_labels)
    return status_instance