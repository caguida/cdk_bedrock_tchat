import streamlit as st
import requests
import json
import time

from configs import *

from PIL import Image
image = Image.open("./img/sagemaker.png")
st.image(image, width=80)
st.header("Text Generation")
st.caption("Using FLAN-T5-XL model from Hugging Face")

conversation = """Customer: Hi there, I'm having a problem with my iPhone.
Agent: Hi! I'm sorry to hear that. What's happening?
Customer: The phone is not charging properly, and the battery seems to be draining very quickly. I've tried different charging cables and power adapters, but the issue persists.
Agent: Hmm, that's not good. Let's try some troubleshooting steps. Can you go to Settings, then Battery, and see if there are any apps that are using up a lot of battery life?
Customer: Yes, there are some apps that are using up a lot of battery.
Agent: Okay, try force quitting those apps by swiping up from the bottom of the screen and then swiping up on the app to close it.
Customer: I did that, but the issue is still there.
Agent: Alright, let's try resetting your iPhone's settings to their default values. This won't delete any of your data. Go to Settings, then General, then Reset, and then choose Reset All Settings.
Customer: Okay, I did that. What's next?
Agent: Now, let's try restarting your iPhone. Press and hold the power button until you see the "slide to power off" option. Slide to power off, wait a few seconds, and then turn your iPhone back on.
Customer: Alright, I restarted it, but it's still not charging properly.
Agent: I see. It looks like we need to run a diagnostic test on your iPhone. Please visit the nearest Apple Store or authorized service provider to get your iPhone checked out.
Customer: Do I need to make an appointment?
Agent: Yes, it's always best to make an appointment beforehand so you don't have to wait in line. You can make an appointment online or by calling the Apple Store or authorized service provider.
Customer: Okay, will I have to pay for the repairs?
Agent: That depends on whether your iPhone is covered under warranty or not. If it is, you won't have to pay anything. However, if it's not covered under warranty, you will have to pay for the repairs.
Customer: How long will it take to get my iPhone back?
Agent: It depends on the severity of the issue, but it usually takes 1-2 business days.
Customer: Can I track the repair status online?
Agent: Yes, you can track the repair status online or by calling the Apple Store or authorized service provider.
Customer: Alright, thanks for your help.
Agent: No problem, happy to help. Is there anything else I can assist you with?
Customer: No, that's all for now.
Agent: Alright, have a great day and good luck with your iPhone!"""

with st.spinner("Retrieving configurations..."):

    all_configs_loaded = False

    while not all_configs_loaded:
        try:
            api_endpoint = "https://cal5fggwk2.execute-api.eu-west-1.amazonaws.com/prod/"#get_parameter(key_txt2nlu_api_endpoint)
            sm_endpoint = "model Falcon"#get_parameter(key_txt2nlu_sm_endpoint)
            all_configs_loaded = True
        except:
            time.sleep(5)

    endpoint_name = st.sidebar.text_input("SageMaker Endpoint Name:",sm_endpoint)
    url = st.sidebar.text_input("API GW Url:",api_endpoint)

    context = st.text_area("Input Context:", conversation, height=300)


    queries = ("write a summary",
                "What steps were suggested to the customer to fix the issue?",
                "What is the overall sentiment and sentiment score of the conversation between the customer and the agent?")

    selection = st.selectbox(
        "Select a query:", queries)

    if st.button("Generate Response", key=selection):
        if endpoint_name == "" or selection == "" or url == "":        
            st.error("Please enter a valid endpoint name, API gateway url and prompt!")
        else:
            with st.spinner("Wait for it..."):
                try:
                    prompt = f"{context}\n{selection}"
                    r = requests.post(url,json={"inputs":prompt, "endpoint_name":endpoint_name},timeout=180)
                    data = r.json()
                    generated_text = data["generated_text"]
                    st.write(generated_text)
                    
                except requests.exceptions.ConnectionError as errc:
                    st.error("Error Connecting:",errc)
                    
                except requests.exceptions.HTTPError as errh:
                    st.error("Http Error:",errh)
                    
                except requests.exceptions.Timeout as errt:
                    st.error("Timeout Error:",errt)    
                    
                except requests.exceptions.RequestException as err:
                    st.error("OOps: Something Else",err)                
                                        
            st.success("Done!")

    query = st.text_area("Input Query:", "what do you suggest as next step for the customer?")

    if st.button("Generate Response", key=query):
        if endpoint_name == "" or query == "" or url == "":        
            st.error("Please enter a valid endpoint name, API gateway url and query!")
        else:
            with st.spinner("Wait for it..."):
                try:
                    prompt = f"{context}\n{query}"
                    r = requests.post(url,json={"inputs":prompt, "endpoint_name":endpoint_name},timeout=180)
                    data = r.json()
                    generated_text = data["generated_text"]
                    st.write(generated_text)
                    
                except requests.exceptions.ConnectionError as errc:
                    st.error("Error Connecting:",errc)
                    
                except requests.exceptions.HTTPError as errh:
                    st.error("Http Error:",errh)
                    
                except requests.exceptions.Timeout as errt:
                    st.error("Timeout Error:",errt)    
                    
                except requests.exceptions.RequestException as err:
                    st.error("OOps: Something Else",err)                
                                
            st.success("Done!")
        
