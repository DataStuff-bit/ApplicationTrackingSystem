# Import necessary libraries
import os
import io
import base64
from PIL import Image
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as ai
import fitz  # PyMuPDF

# Load environment variables
load_dotenv()

# Configure the API key
ai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def get_gemini_response(input_text, pdf_content, prompt):
    model = ai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input_text, pdf_content[0], prompt])
    return response.text


def input_pdf_setup(upload_file):
    # Convert the PDF to image using PyMuPDF
    if upload_file is not None:
        pdf_bytes = upload_file.read()
        pdf_document = fitz.open(stream=io.BytesIO(pdf_bytes), filetype="pdf")
        images = []
        img_byte_arrs = []

        for page_number in range(len(pdf_document)):
            page = pdf_document.load_page(page_number)
            pix = page.get_pixmap()
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            images.append(img)

            # Convert to bytes
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format="JPEG")
            img_byte_arrs.append(img_byte_arr.getvalue())

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()
            }
            for img_byte_arr in img_byte_arrs
        ]

        pdf_document.close()
        return pdf_parts
    else:
        raise FileNotFoundError("No File Uploaded")


# Streamlit App
st.set_page_config(page_title="ATS_RESUME_EXPERT")
st.header("ATS Tracking system")
input_text = st.text_area("Job Description:", key="input")
upload_file = st.file_uploader("Upload your resume (PDF).....", type=["pdf"])

if upload_file is not None:
    st.write("PDF Uploaded Successfully")

submit1 = st.button("Tell Me About the Resume")
submit2 = st.button("How can I improvise my skills")
submit3 = st.button("Percentage Match")

input_prompt1 = """
You are an experienced HR with Tech Experience in the field of Data Science, Full Stack Web Development,
Big Data Engineering, DEVOPS, Data Analyst. Your task is to review the provided resume against ...

# Add input_prompt2 and input_prompt3 similarly

"""
input_prompt2 = """
You are a technical Human Resource Manager with expertise in the field of Data Science, Full Stack Web Development,
Big Data Engineering, DEVOPS, Data Analyst. Your role is to scrutinize the resume in light of the job description provided.
Share your thoughts and insights on the candidate's suitability for the role from an HR perspective.
Additionally, offer advice on enhancing the candidate's skills and identify areas where to improve.
"""
input_prompt3 = """
You are a skilled ATS (Application Tracking System) scanner with a deep understanding of Data Science, Full Stack Web Development,
Big Data Engineering, DEVOPS, Data Analyst, and deep ATS functionality. Your task is to evaluate the resume against the provided job description,
give me the percentage match of the job description. First, the output should come, then the keywords, and lastly the final thoughts.
"""

# Initialize the model here

if submit1:
    if upload_file is not None:
        pdf_content = input_pdf_setup(upload_file)
        response = get_gemini_response(input_text, pdf_content, input_prompt1)
        st.subheader("The response is")
        st.write(response)
    else:
        st.write("Pls Upload Resume")

elif submit2:
    if upload_file is not None:
        pdf_content = input_pdf_setup(upload_file)
        response = get_gemini_response(input_text, pdf_content, input_prompt2)
        st.subheader("The response is")
        st.write(response)
    else:
        st.write("Pls Upload Resume")

elif submit3:
    if upload_file is not None:
        pdf_content = input_pdf_setup(upload_file)
        response = get_gemini_response(input_text, pdf_content, input_prompt3)
        st.subheader("The response is")
        st.write(response)
    else:
        st.write("Pls Upload Resume")
