import streamlit as st
import google.generativeai as genai
from prompts import ai_roadmap_prompt

# session variables
if "user_input" not in st.session_state:
    st.session_state.user_input = ''

if "response_text" not in st.session_state:
    st.session_state.response_text = ''

# Configure the API key
genai.configure(api_key='AIzaSyBYiBR0hyxwtZb4KcEBUcyCfJehMA-7fiw')

# Model setup
model_list = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-2.0-flash-exp']
model = genai.GenerativeModel(
    model_name=model_list[2],
    system_instruction="You're a Roadmap generator for Tools, Technology and Programming"
)

#Generating Markdown
def generate_md(content,file_name):
    with open(f'{file_name}.md','w',encoding='utf-8') as f:
        f.write(content)

#Set Up Streamlit Page:
st.set_page_config(layout='centered')

st.title('AI Roadmap Generator')
st.write('Your personalized AI learning guide generator.')


user_input = st.text_area("User Input", label_visibility='hidden', 
                          placeholder='I wanna learn about..', 
                          value=st.session_state.user_input, key='user_input')

prompt_message = ai_roadmap_prompt + "\n" + user_input

# layout for buttons
bl1, bl2, bl3, bl4 = st.columns([1, 1, 1, 1])

with bl1:
    create_roadmap = st.button('Create Roadmap', type='primary')
with bl2:
    save_as_md = st.button('Save as Markdown')
with bl4:
    reset = st.button('Reset')


if create_roadmap:
    st.session_state.response_text = ''
    with st.spinner('Generating Roadmap..'):        #loading
        response = model.generate_content(prompt_message)
        st.session_state.response_text += response.text
        st.markdown(st.session_state.response_text, unsafe_allow_html=True)

if save_as_md:
    if st.session_state.response_text.strip():
        generate_md(st.session_state.response_text, user_input)
        st.success('Markdown file created Successfully!')
    else:
        st.error('No content to save! Please generate the roadmap first.')

if reset:
    st.session_state.response_text = ''
    st.success('Reset Successful!')



