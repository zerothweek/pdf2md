import streamlit as st
from pdf2image import convert_from_bytes
import tempfile
import markdown
import base64

st.set_page_config(layout="wide")
st.title("PDF ↔ Markdown Editor")

# --- File upload
col1, col2 = st.columns([1, 2])
with col1:
    pdf_file = st.file_uploader("Upload PDF", type=["pdf"])
with col2:
    md_file = st.file_uploader("Upload Markdown", type=["md"])

# --- Initialize markdown content
md_text = ""

if md_file:
    md_text = md_file.read().decode("utf-8")

# --- Layout: left (PDF) and right (Markdown)
if pdf_file and md_file:
    col_left, col_right = st.columns([1, 1])

    # PDF viewer: convert PDF pages to images
    with col_left:
        st.subheader("PDF View")
        with st.spinner("Rendering PDF..."):
            images = convert_from_bytes(pdf_file.read())
            for i, img in enumerate(images):
                st.image(img, caption=f"Page {i+1}", use_column_width=True)

    # Markdown editor + preview
    with col_right:
        st.subheader("Markdown Editor")
        edited_md = st.text_area("Edit the Markdown", value=md_text, height=400, key="editor")

        st.subheader("Markdown Preview")
        st.markdown(edited_md, unsafe_allow_html=True)

        # Download button
        b64 = base64.b64encode(edited_md.encode()).decode()
        href = f'<a href="data:file/text;base64,{b64}" download="corrected.md">Download Corrected Markdown</a>'
        st.markdown(href, unsafe_allow_html=True)