import streamlit as st
import anthropic
import base64
import re

# Set up the page
st.set_page_config(page_title="Interactive Study Dashboard", layout="wide")

# Streamlit app
st.title("Interactive Study Dashboard Generator")

# User input
subject = st.text_area("Masukkan topik yang ingin Anda pelajari:")

# Function to get response from Claude API and extract only HTML
def get_claude_response(subject, part, context=""):
    client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
    
    base_prompt = f"""create an interactive and simple dashboard to present and study {subject} so that I can understand well, make it really aesthetic and elegant. with aesthetic design and icons. the material should be explain with creative most related simulation. create in html. make sure there is no error. berbahasa Indonesia. respond only with html script, no other explanation, just html script directly. buat design-nya estetic dan berwarna.

generate dalam 3 bagian script, setiap bagian tidak bisa langsung dirunning, tapi jika nanti langsung digabung tidak error.
sekarang tulis dulu bagian {part}."""

    if context:
        if part == 2:
            full_prompt = base_prompt + f" Berikut adalah bagian pertama yang sudah dibuat: {context}"
        elif part == 3:
            full_prompt = base_prompt + f" Berikut adalah bagian pertama dan kedua yang sudah dibuat: {context}"
    else:
        full_prompt = base_prompt

    try:
        message = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=4000,
            temperature
