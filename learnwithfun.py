import streamlit as st
import anthropic
import base64
import PyPDF2
import io

# Set up the page
st.set_page_config(page_title="Interactive Paper Summary Dashboard", layout="wide")

# Streamlit app
st.title("Interactive Paper Summary Dashboard Generator")

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# Function to get response from Claude API
def get_claude_response(paper_content):
    client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
    
    try:
        message = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=4000,
            temperature=0,
            messages=[
                {
                    "role": "user",
                    "content": f"create an interactive and super detailed dashboard to present and study this paper so that i can really understand the method and the results, make it really good and professional. with aesthetic design and icons. create in html. make sure there is no error. berbahasa Indonesia. paper contents: {paper_content}"
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

# File uploader for PDF
uploaded_file = st.file_uploader("Unggah file PDF paper Anda", type="pdf")

# Generate and display dashboard when user clicks the button
if st.button("Buat Dashboard"):
    if uploaded_file is not None:
        with st.spinner("Sedang memproses PDF dan membuat dashboard Anda..."):
            # Extract text from PDF
            pdf_content = extract_text_from_pdf(uploaded_file)
            
            # Get response from Claude
            raw_content = get_claude_response(pdf_content)
            
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
        st.warning("Silakan unggah file PDF paper yang ingin dirangkum.")

# Instructions for use
st.markdown("""
## Cara Penggunaan:
1. Unggah file PDF paper yang ingin Anda rangkum menggunakan tombol unggah di atas.
2. Klik tombol "Buat Dashboard".
3. Tunggu beberapa saat sementara PDF diproses dan dashboard interaktif dibuat.
4. Jelajahi dashboard yang dihasilkan di dalam iframe. Jika kontennya panjang, Anda dapat menggulir ke bawah di dalam iframe.
5. Gunakan link "Download HTML" untuk menyimpan dashboard sebagai file HTML.
6. Jika Anda menemui masalah, periksa HTML mentah di bagian expander untuk debugging.

Catatan: Pembuatan mungkin memerlukan beberapa saat tergantung pada kompleksitas dan panjang paper.
""")
