import streamlit as st
import requests
import anthropic

# Set up the page
st.set_page_config(page_title="Interactive Study Dashboard", layout="wide")

# Streamlit app
st.title("Interactive Study Dashboard Generator")

# User input
subject = st.text_area("Enter the subject you want to study (put up to 3 words):")

# Function to get response from Claude API
def get_claude_response(subject):
    client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
    
    prompt = f"create an interactive and super detailed dashboard to present and study {subject} so that I can understand well, make it really good and professional. with aesthetic design and icons. the material should be explain with creative and out of the box. create in html. make sure there is no error. berbahasa Indonesia. respond only with html script, no other explanation, just html script directly."
    
    try:
        response = client.completions.create(
            model="claude-3-sonnet-20240229",
            prompt=prompt,
            max_tokens_to_sample=100000,
        )
        return response.completion
    except Exception as e:
        return str(e)

# Generate and display dashboard when user clicks the button
if st.button("Generate Dashboard"):
    if subject:
        with st.spinner("Generating your dashboard..."):
            html_content = get_claude_response(subject)
            
        # Display the generated HTML
        st.components.v1.html(html_content, height=600, scrolling=True)
    else:
        st.warning("Please enter a subject to study.")

# Instructions for use
st.markdown("""
## How to use:
1. Enter the subject you want to study in the text area above.
2. Click the "Generate Dashboard" button.
3. Wait for the interactive dashboard to be generated and displayed.
4. Scroll through the dashboard to explore the content.

Note: Generation may take a few moments depending on the complexity of the subject.
""")
