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
            full_prompt = base_prompt + f"\n\nBerikut adalah bagian pertama yang sudah dibuat:\n\n{context}"
        elif part == 3:
            full_prompt = base_prompt + f"\n\nBerikut adalah bagian pertama dan kedua yang sudah dibuat:\n\n{context}"
    else:
        full_prompt = base_prompt

    try:
        message = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=4000,
            temperature=0,
            messages=[
                {
                    "role": "user",
                    "content": full_prompt
                }
            ]
        )
        # Extract only the HTML content
        content = message.content
        if isinstance(content, list):
            content = ' '.join(str(item) for item in content)
        html_content = extract_html(content)
        return html_content
    except Exception as e:
        st.error(f"Terjadi kesalahan saat memanggil API Claude: {str(e)}")
        return None

# Function to extract only HTML content
def extract_html(content):
    # Remove any text before the first < and after the last >
    html_content = re.search(r'<[\s\S]*>', content)
    if html_content:
        return html_content.group(0)
    return content  # Return original content if no HTML tags found

# Function to create a download link for HTML content
def get_html_download_link(html_string, filename="dashboard.html"):
    b64 = base64.b64encode(html_string.encode()).decode()
    href = f'<a href="data:text/html;base64,{b64}" download="{filename}">Download HTML</a>'
    return href

# Generate and display dashboard when user clicks the button
if st.button("Buat Dashboard"):
    if subject:
        with st.spinner("Sedang membuat dashboard Anda..."):
            # Generate part 1
            part1 = get_claude_response(subject, 1)
            if not part1:
                st.error("Gagal menghasilkan bagian pertama. Silakan coba lagi.")
                st.stop()

            # Generate part 2 with full context from part 1
            part2 = get_claude_response(subject, 2, context=part1)
            if not part2:
                st.error("Gagal menghasilkan bagian kedua. Silakan coba lagi.")
                st.stop()

            # Generate part 3 with full context from parts 1 and 2
            part3 = get_claude_response(subject, 3, context=part1 + "\n\n" + part2)
            if not part3:
                st.error("Gagal menghasilkan bagian ketiga. Silakan coba lagi.")
                st.stop()

            # Combine all parts
            full_html = f"{part1}\n{part2}\n{part3}"

            # Remove any comments or labels from the HTML
            full_html = re.sub(r'<!--.*?-->', '', full_html, flags=re.DOTALL)
            full_html = re.sub(r'<!-- Bagian \d -->', '', full_html)

            # Display the combined dashboard
            iframe_content = f"""
            <iframe srcdoc='{full_html}' 
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
            st.markdown(get_html_download_link(full_html), unsafe_allow_html=True)
            
            # Show raw HTML for debugging in an expander
            with st.expander("Lihat HTML Mentah (untuk debugging)"):
                st.text_area("Raw HTML:", value=full_html, height=300)
    else:
        st.warning("Silakan masukkan topik yang ingin dipelajari.")

# Instructions for use
st.markdown("""
## Cara Penggunaan:
1. Masukkan topik yang ingin Anda pelajari di area teks di atas.
2. Klik tombol "Buat Dashboard".
3. Tunggu beberapa saat sementara dashboard interaktif dibuat dalam tiga bagian.
4. Jelajahi dashboard yang dihasilkan di dalam iframe. Jika kontennya panjang, Anda dapat menggulir ke bawah di dalam iframe.
5. Gunakan link "Download HTML" untuk menyimpan dashboard sebagai file HTML.
6. Jika Anda menemui masalah, periksa HTML mentah di bagian expander untuk debugging.

Catatan: Pembuatan mungkin memerlukan waktu lebih lama karena dilakukan dalam tiga tahap dengan konteks lengkap.
""")
