import streamlit as st
import anthropic
import base64

# Set up the page
st.set_page_config(page_title="Interactive Study Dashboard", layout="wide")

# Streamlit app
st.title("Interactive Study Dashboard Generator")

# User input
subject = st.text_area("Masukkan topik yang ingin Anda pelajari:")

# Function to get response from Claude API
def get_claude_response(subject):
    client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
    
    try:
        message = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=4000,
            temperature=0,
            messages=[
                {
                    "role": "user",
                    "content": f"create an interactive and simple dashboard to present and study {subject} so that I can understand well, make it really aesthetic and elegant. with aesthetic design and icons. the material should be explain with creative most related simulation. create in html. make sure there is no error. berbahasa Indonesia. respond only with html script, no other explanation, just html script directly. buat design-nya estetic dan berwarna."
                }
            ]
        )
        return message.content
    except Exception as e:
        st.error(f"Terjadi kesalahan saat memanggil API Claude: {str(e)}")
        return None

# Function to extract HTML from TextBlock objects
def extract_html_from_textblocks(content):
    if isinstance(content, list) and len(content) > 0 and hasattr(content[0], 'text'):
        return content[0].text
    return content

# Function to create a download link for HTML content
def get_html_download_link(html_string, filename="dashboard.html"):
    b64 = base64.b64encode(html_string.encode()).decode()
    href = f'<a href="data:text/html;base64,{b64}" download="{filename}">Download HTML</a>'
    return href

# Generate and display dashboard when user clicks the button
if st.button("Buat Dashboard"):
    if subject:
        with st.spinner("Sedang membuat dashboard Anda..."):
            raw_content = get_claude_response(subject)
            
        if raw_content:
            html_content = extract_html_from_textblocks(raw_content)
            if html_content:
                # Wrap the content in an iframe with sandbox attribute
                iframe_content = f"""
                <iframe srcdoc='{html_content}' 
                        width="100%" 
                        height="600px" 
                        style="border: none;"
                        sandbox="allow-scripts allow-same-origin">
                </iframe>
                """
                st.components.v1.html(iframe_content, height=620, scrolling=True)
                
                # Add a note about scrolling
                st.info("Jika konten lebih panjang, Anda dapat menggulir ke bawah di dalam dashboard.")
                
                # Provide a download link for the HTML
                st.markdown(get_html_download_link(html_content), unsafe_allow_html=True)
                
                # Always show raw HTML for debugging in an expander
                with st.expander("Lihat HTML Mentah (untuk debugging)"):
                    st.text_area("Raw HTML:", value=html_content, height=300)
            else:
                st.error("Tidak dapat mengekstrak konten HTML yang valid. Berikut adalah konten mentahnya:")
                st.text_area("Konten Mentah:", value=str(raw_content), height=300)
        else:
            st.error("Gagal menghasilkan konten dashboard. Silakan coba lagi.")
    else:
        st.warning("Silakan masukkan topik yang ingin dipelajari.")

# Instructions for use
st.markdown("""
## Cara Penggunaan:
1. Masukkan topik yang ingin Anda pelajari di area teks di atas.
2. Klik tombol "Buat Dashboard".
3. Tunggu beberapa saat sementara dashboard interaktif dibuat.
4. Jelajahi dashboard yang dihasilkan di dalam iframe. Jika kontennya panjang, Anda dapat menggulir ke bawah di dalam iframe.
5. Gunakan link "Download HTML" untuk menyimpan dashboard sebagai file HTML.
6. Jika Anda menemui masalah, periksa HTML mentah di bagian expander untuk debugging.

Catatan: Pembuatan mungkin memerlukan beberapa saat tergantung pada kompleksitas topik.
""")
