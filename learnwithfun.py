import streamlit as st
import anthropic

# Set up the page
st.set_page_config(page_title="Interactive Study Dashboard", layout="wide")

# Streamlit app
st.title("Interactive Study Dashboard Generator")

# User input
subject = st.text_area("Enter the subject you want to study:")

# Function to get response from Claude API
def get_claude_response(subject):
    client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
    
    try:
        message = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=100000,
            temperature=0,
            messages=[
                {
                    "role": "user",
                    "content": f"create an interactive and super detailed dashboard to present and study {subject} so that I can understand well, make it really good and professional. with aesthetic design and icons. the material should be explain with creative and out of the box. create in html. make sure there is no error. berbahasa Indonesia. respond only with html script, no other explanation, just html script directly."
                }
            ]
        )
        return message.content
    except Exception as e:
        st.error(f"An error occurred while calling the Claude API: {str(e)}")
        return None

# Generate and display dashboard when user clicks the button
if st.button("Generate Dashboard"):
    if subject:
        with st.spinner("Generating your dashboard..."):
            html_content = get_claude_response(subject)
            
        if html_content:
            # Ensure the content is a string and starts with <html>
            if isinstance(html_content, str) and html_content.strip().lower().startswith("<html"):
                # Display the generated HTML
                try:
                    st.components.v1.html(html_content, height=600, scrolling=True)
                except Exception as e:
                    st.error(f"Error displaying HTML content: {str(e)}")
                    st.text_area("Raw HTML Content:", value=html_content, height=300)
            else:
                st.error("The generated content is not valid HTML. Here's the raw content:")
                st.text_area("Raw Content:", value=html_content, height=300)
        else:
            st.error("Failed to generate dashboard content. Please try again.")
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
