import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf

from dotenv import load_dotenv

load_dotenv() ## load all the environment variables

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Gemini Pro Response
def get_gemini_response(input):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input)
    return response.text

# def input_pdf_text(uploaded_file):
#     reader = pdf.PdfReader(uploaded_file)
#     text = ""
#     for page in len(reader.pages):
#         page = reader.pages[page]
#         text += str(page.extract_text)
#     return text

def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        text += str(reader.pages[page].extract_text())
    return text

## Prompt template
input_prompt="""
Hey Act like a skilled or very experience ATS (Application Tracking System) with a deep understanding of
tech field, software engineering, data science, data analyst and big data engineer. Your task is to 
evaluate the resume based on the given job description. You must consider the job market is very
competitive and you should provide best assistance for improving the resumes. Assign the percentage
matching based on jd and the missing keywords with high accuracy
Resume: {text}
Description: {jd}

I want the reponse in one single sting having the structure
{{"JD Match":"%","MissingKeywords:[]", "Profile Summary":""}}
"""

## Streamlit app
st.title("Smart ATS")
st.text("Improve your Resume ATS")
jd = st.text_area("Paste the job description")
uploaded_file = st.file_uploader("Upload your resume",type = "pdf", help = "Please upload the pdf")

submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        text = input_pdf_text(uploaded_file)
        # Replace the placeholder in the prompt with the actual resume text
        prompt_with_resume = input_prompt.format(text=text, jd=jd)

        response = get_gemini_response(prompt_with_resume)
        st.subheader(response)