import streamlit as st
import openai as op

op.api_key = st.secrets["OPENAI_API_KEY"]

st.title("WINWIN STUDIO AI")

st.write("")

with st.form(key='prompt_form'):
    prompt_input = st.text_input(label='Enter your prompt', placeholder='Enter your prompt')
    selected_size = st.selectbox("Size", ["256x256", "512x512", "1024x1024"])
    submit_button = st.form_submit_button(label='Submit')
    
if submit_button and prompt_input:
    gpt_prompt = [{
        "role": "system",
        "content": "Imagine the detail appearance of the input. Response it around 20 words."
    }]
    
    gpt_prompt.append({
        "role": "user",
        "content": prompt_input
    })
    
    with st.spinner(text='Generating prompt...'):
        gpt_response = op.ChatCompletion.create(
            model = "gpt-3.5-turbo",
            messages=gpt_prompt
        )
    
    prompt_from_gpt = gpt_response.choices[0]["message"]["content"]
    
    st.write(prompt_from_gpt)
    st.write("")
    
    with st.spinner(text='Generating image...'):
        dalle_response = op.Image.create(
            prompt = prompt_from_gpt, 
            size = selected_size
        )
    
    st.image(dalle_response["data"][0]["url"])
    