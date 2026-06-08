import streamlit as st
import PyPDF2
import io
import os
from openai import OpenAI
from dotenv import load_dotenv
from langchain_ollama import ChatOllama

load_dotenv()
st.set_page_config(page_title = "AI Resume Critiquer", page_icon = "📃", layout = "centered")
st.title("AI Resume Critiquer")
st.markdown("Upload your resume in PDF format and receive personalized feedback to enhance your job application.")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

uploaded_file = st.file_uploader("Upload your resume (PDF or TXT)", type=["pdf", "txt"])
job_role = st.text_input("Enter the job role you are applying for (optional)")
analyze = st.button("Analyze Resume")
def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text
def extract_text_from_file(uploaded_file):
    if uploaded_file.type == "application/pdf":
        return extract_text_from_pdf(io.BytesIO(uploaded_file.read()))
    return uploaded_file.read().decode("utf-8")
   
if analyze and uploaded_file:
    st.write("Button clicked, processing the resume...")
    try:
        file_content = extract_text_from_file(uploaded_file)
        st.write("PDF extracted successfully.")
        st.write(file_content[:500])

        if not file_content.strip():
            st.error("The uploaded file is empty. Please upload a valid resume.")
            st.stop()
      
        prompt = f"""Please review the following resume and provide feedback on how to improve it for a job application.
        focus on the following aspects:
        - Clarity and conciseness
        - Relevance to the job role
        - Formatting and layout
        - self improvement for {job_role if job_role else 'general job applications'}
          
        Resume Content:
        {file_content}
        please provide specific suggestions for improvement and highlight any areas that may need more detail or clarification."""
        
        llm = ChatOllama(model="qwen3:latest", temperature = 0.7)
        st.write("Sending prompt to ollama...")
        response = llm.invoke(prompt)
        st.write("Received response from ollama.")
        st.markdown("### Analysis results")
        st.markdown(response.content)
    except Exception as e:
        st.error(f"An error occurred while processing the resume: {str(e)}")

