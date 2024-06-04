from openai import OpenAI
import time

api_key = "sk-proj-zDUnIGcBEDeJrfuHRpM5T3BlbkFJae780zLmc88IgXOhcfLT"
assistant_id = "asst_gm882hLbHFU3zlUN8G5bijfE"


client = OpenAI(api_key=api_key)
thread = client.beta.threads.create()
thread_id = thread.id

user_message = "Give me the top 5 best bets for the NHL playoffs tomorrow"

message = client.beta.threads.messages.create(thread_id=thread_id, role="user", content=user_message)


## Run 1 - Retrieve Data
asst_message1 = "STEP 1: Identify Key Information"
asstmessage1 = client.beta.threads.messages.create(thread_id=thread_id, role="assistant", content=asst_message1)
run1 = client.beta.threads.runs.create(thread_id=thread_id, assistant_id=assistant_id, tool_choice="none")
run1id = run1.id
while run1.status != "completed":
    time.sleep(2)
    run1 = client.beta.threads.runs.retrieve(run_id=run1id, thread_id=thread_id)
    if run1.status =="completed":
        break




## Run 2
asst_message2 = "STEP 2: Retrieve data using File Search"
asstmessage2 = client.beta.threads.messages.create(thread_id=thread_id, role="assistant", content=asst_message2)
run2 = client.beta.threads.runs.create(thread_id=thread_id, assistant_id=assistant_id, tool_choice={"type": "file_search"})
while run2.status != "completed":
    time.sleep(2)
    run2 = client.beta.threads.runs.retrieve(run_id=run2.id, thread_id=thread_id)
    if run2.status =="completed":
        break



## Run 3
asst_message3 = "STEP 3: Create Algorithm and Variables Using Code Interpreter and attached files as examples only"
asstmessage3= client.beta.threads.messages.create(thread_id=thread_id, role="assistant", content=asst_message3)
run3 = client.beta.threads.runs.create(thread_id=thread_id, assistant_id=assistant_id, tool_choice={"type": "code_interpreter"})
while run3.status != "completed":
    time.sleep(2)
    run3 = client.beta.threads.runs.retrieve(run_id=run3.id, thread_id=thread_id)
    if run3.status =="completed":
        break



## Run 4
asst_message4 = "STEP 4: Run Simulation 100 times and return a summary result"
asstmessage4 = client.beta.threads.messages.create(thread_id=thread_id, role="assistant", content=asst_message4)
run4 = client.beta.threads.runs.create(thread_id=thread_id, assistant_id=assistant_id, tool_choice={"type": "code_interpreter"})
while run4.status != "completed":
    time.sleep(2)
    run4 = client.beta.threads.runs.retrieve(run_id=run4.id, thread_id=thread_id)
    if run4.status =="completed":
        break

thread_message_list = client.beta.threads.messages.list(thread_id=thread_id)
for thread_message in thread_message_list:
    if thread_message.role == "assistant" and thread_message.run_id == run4.id:
        thread_message_content = thread_message.content[0].text.value
        print(thread_message_content)