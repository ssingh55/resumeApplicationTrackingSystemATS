## 1. Field to put my job description
## 2. Upload pdf
## 3. pdf to image -->processing-> Google gemini pro
## 4. Prompts Template [Multiple prompt]
from dotenv import load_dotenv

load_dotenv()

import streamlit as st
import os
import pdf2image
import google.generativeai as genai
import io
import base64
from PIL import Image

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

def get_gemini_response(input,pdf_content,prompt):
    model=genai.GenerativeModel('gemini-pro-vision')
    response=model.generate_content([input,pdf_content[0],prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        ## Convert the pdf to image
        images=pdf2image.convert_from_bytes(uploaded_file.read())

        first_page=images[0]

        ## Convert to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format="JPEG")
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode() # encode to base64
            }
        ]

        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")
    
## Streamilit App
    
st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System")
input_text=st.text_area("Job Description: ",key="input")
uploaded_file=st.file_uploader("Upload your resume(PDF)...",type=["pdf"])

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

submit1 = st.button("Tell me About the Resume")

submit2 = st.button("How can I Improvise my Skills")

submit3 = st.button("Percentage match")

input_prompt1 = """
You are an experienced HR with tech experience in the field of any one job role from Data Science, 
Full Stack web development,devops, big data engineering,Data Analyst, your task is to review the 
provided resume against the job description for these profiles.
Please share your professional evaluation on whether the candidate's profile aligns with the role.
Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements
"""

input_prompt2="""
Act as a Technical Human Resource Manager and provide guidance on how to improve skills in a 
specific field based on the user's job description. Conduct a comprehensive analysis of the 
user's current skills and competencies, as well as the requirements and trends within their 
industry. Prepare a detailed plan outlining specific areas of improvement, suggesting relevant 
courses or certifications, and providing resources for self-learning. Additionally, offer advice 
on networking opportunities, mentorship programs, and professional development activities that 
can accelerate skill growth. Ensure that the recommendations align with the user's career goals 
and provide a clear roadmap for skill enhancement.
"""

input_prompt3="""
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of any one job role 
Data Science,Full Stack web development,devops, big data engineering,Data Analyst and deep ATS functionality,
 your task is to evaluate the resume against the provided job description. Give me the percentage of 
 match if the resume matches the job description.First the output come should come as percentage and 
 then keywords missing and last final thoughts.
"""

if submit1:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt1,pdf_content,input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload the resume")

elif submit2:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt2,pdf_content,input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload the resume")

elif submit3:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt3,pdf_content,input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload the resume")

