import streamlit as st
from PyPDF2 import PdfReader, PdfWriter
import os

def parse_ranges(pages_str):
    pages = []
    for part in pages_str.split(','):
        part = part.strip()
        if '~' in part:
            start, end = map(int, part.split('~'))
            pages.extend(range(start - 1, end))  # 0-based indexing
        else:
            pages.append(int(part) - 1)
    return pages

def save_cut(reader, pages_str, output_name, output_dir):
    writer = PdfWriter()
    pages = parse_ranges(pages_str)
    for page in pages:
        if 0 <= page < len(reader.pages):
            writer.add_page(reader.pages[page])
    output_path = os.path.join(output_dir, output_name)
    with open(output_path, "wb") as f:
        writer.write(f)
    return output_path

st.title("PDF Page Splitter")

pdf_file = st.file_uploader("Upload a PDF", type=["pdf"])
output_root = st.text_input("Root output directory", value="output")

if pdf_file:
    reader = PdfReader(pdf_file)
    total_pages = len(reader.pages)
    st.info(f"PDF has {total_pages} pages.")

    cuts = []
    num_cuts = st.number_input("Number of cuts", min_value=1, step=1, value=1)

    for i in range(num_cuts):
        st.markdown(f"**Cut {i+1}**")
        col1, col2, col3 = st.columns(3)
        with col1:
            pages = st.text_input(f"Pages for cut {i+1}", key=f"pages_{i}", placeholder="e.g. 1~5, 7")
        with col2:
            name = st.text_input(f"Filename for cut {i+1}", key=f"name_{i}", placeholder="cut1.pdf")
        with col3:
            directory = st.text_input(f"Directory for cut {i+1}", key=f"dir_{i}", value="dir1")
        if pages and name and directory:
            cuts.append((pages, name, directory))

    if st.button("Split and Save"):
        os.makedirs(output_root, exist_ok=True)
        for pages_str, filename, sub_dir in cuts:
            dir_path = os.path.join(output_root, sub_dir)
            os.makedirs(dir_path, exist_ok=True)
            output_path = save_cut(reader, pages_str, filename, dir_path)
            st.success(f"Saved to: {output_path}")