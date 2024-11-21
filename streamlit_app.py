import streamlit as st
from PyPDF2 import PdfReader, PdfWriter
from pdf2docx import Converter
from fpdf import FPDF
from io import BytesIO
import os

# Helper function to save uploaded files temporarily
def save_uploadedfile(uploadedfile, filename="temp.pdf"):
    with open(filename, "wb") as f:
        f.write(uploadedfile.getbuffer())

# PDF to Word Converter
def pdf_to_word(pdf_file):
    save_uploadedfile(pdf_file, "temp.pdf")
    converter = Converter("temp.pdf")
    converter.convert("converted_document.docx")
    converter.close()
    os.remove("temp.pdf")
    return "converted_document.docx"

# PDF Encryption
def encrypt_pdf(pdf_file, password):
    save_uploadedfile(pdf_file, "unencrypted_temp.pdf")
    reader = PdfReader("unencrypted_temp.pdf")
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)
    writer.encrypt(password)
    encrypted_pdf_path = "encrypted_document.pdf"
    with open(encrypted_pdf_path, "wb") as encrypted_pdf:
        writer.write(encrypted_pdf)
    os.remove("unencrypted_temp.pdf")
    return encrypted_pdf_path

# PDF Decryption
def decrypt_pdf(pdf_file, password):
    save_uploadedfile(pdf_file, "encrypted_temp.pdf")
    reader = PdfReader("encrypted_temp.pdf")
    if not reader.is_encrypted:
        st.warning("This PDF is not encrypted.")
        return None
    try:
        reader.decrypt(password)
        writer = PdfWriter()
        for page in reader.pages:
            writer.add_page(page)
        decrypted_pdf_path = "decrypted_document.pdf"
        with open(decrypted_pdf_path, "wb") as decrypted_pdf:
            writer.write(decrypted_pdf)
        os.remove("encrypted_temp.pdf")
        return decrypted_pdf_path
    except Exception as e:
        st.error("Decryption failed. Please check the password.")
        os.remove("encrypted_temp.pdf")
        return None

# PDF Merging
def merge_pdfs(pdf_files):
    writer = PdfWriter()
    for file in pdf_files:
        save_uploadedfile(file, "temp.pdf")
        reader = PdfReader("temp.pdf")
        for page in reader.pages:
            writer.add_page(page)
        os.remove("temp.pdf")
    merged_pdf_path = "merged_document.pdf"
    with open(merged_pdf_path, "wb") as merged_pdf:
        writer.write(merged_pdf)
    return merged_pdf_path

# Streamlit Interface
st.title("Advanced PDF Tools")

# PDF to Word
st.header("PDF to Word Converter")
pdf_file = st.file_uploader("Upload a PDF file to convert to Word", type=["pdf"], key="pdf_to_word_uploader")
if st.button("Convert PDF to Word"):
    if pdf_file:
        word_file = pdf_to_word(pdf_file)
        st.download_button("Download Word Document", word_file, file_name="converted_document.docx")

# PDF Encryption
st.header("PDF Encryption")
pdf_file_encrypt = st.file_uploader("Upload a PDF file to encrypt", type=["pdf"], key="pdf_encrypt_uploader")
password_encrypt = st.text_input("Enter a password for encryption", type="password")
if st.button("Encrypt PDF"):
    if pdf_file_encrypt and password_encrypt:
        encrypted_pdf = encrypt_pdf(pdf_file_encrypt, password_encrypt)
        st.download_button("Download Encrypted PDF", encrypted_pdf, file_name="encrypted_document.pdf")

# PDF Decryption
st.header("PDF Decryption")
pdf_file_decrypt = st.file_uploader("Upload an encrypted PDF file", type=["pdf"], key="pdf_decrypt_uploader")
password_decrypt = st.text_input("Enter the password to decrypt", type="password")
if st.button("Decrypt PDF"):
    if pdf_file_decrypt and password_decrypt:
        decrypted_pdf = decrypt_pdf(pdf_file_decrypt, password_decrypt)
        if decrypted_pdf:
            st.download_button("Download Decrypted PDF", decrypted_pdf, file_name="decrypted_document.pdf")

# PDF Merging
st.header("Merge Multiple PDFs")
pdf_files_merge = st.file_uploader("Upload PDF files to merge", type=["pdf"], accept_multiple_files=True, key="pdf_merge_uploader")
if st.button("Merge PDFs"):
    if pdf_files_merge:
        merged_pdf = merge_pdfs(pdf_files_merge)
        st.download_button("Download Merged PDF", merged_pdf, file_name="merged_document.pdf")

st.info("This app uses `pdf2docx` for Word conversion and `PyPDF2` for encryption, decryption, and merging.")
