import streamlit as st
import anthropic

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
            max_tokens=3000,
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
        st.error(f"Terjadi kesalahan saat memanggil API Claude: {str(e)}")
        return None

# Function to extract HTML from TextBlock objects
def extract_html_from_textblocks(content):
    if isinstance(content, list) and len(content) > 0 and hasattr(content[0], 'text'):
        html_content = content[0].text
        # Check if the HTML is complete
        if '</html>' not in html_content:
            html_content += "\n</body>\n</html>"
        return html_content
    return None

# Generate and display dashboard when user clicks the button
if st.button("Buat Dashboard"):
    if subject:
        with st.spinner("Sedang membuat dashboard Anda..."):
            raw_content = get_claude_response(subject)
            
        if raw_content:
            html_content = extract_html_from_textblocks(raw_content)
            if html_content:
                # Display HTML content with scrolling
                st.components.v1.html(html_content, height=600, scrolling=True)
                
                # Add a note about scrolling
                st.info("Jika konten lebih panjang, Anda dapat menggulir ke bawah di dalam dashboard.")
                
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
4. Jelajahi dashboard yang dihasilkan. Jika kontennya panjang, Anda dapat menggulir ke bawah di dalam dashboard.
5. Jika Anda menemui masalah, periksa HTML mentah di bagian expander untuk debugging.

Catatan: Pembuatan mungkin memerlukan beberapa saat tergantung pada kompleksitas topik.
""")
