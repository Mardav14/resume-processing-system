import openai
import docx2txt
from PyPDF2 import PdfReader
import mimetypes
import os
from dotenv import load_dotenv
from io import BytesIO
import json

from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence

from sentence_transformers import SentenceTransformer, util

load_dotenv() 
# OpenAI API key
os.environ["OPENAI_API_KEY"] = os.getenv("API_KEY")

def read_file(uploaded_file):
    try:
        content_type = uploaded_file.content_type  # Detect MIME type

        if content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            return read_docx(uploaded_file)
        elif content_type == "application/pdf":
            return read_pdf(uploaded_file)
        else:
            return "Unsupported file type"
    except Exception as e:
        return f"Error: {str(e)}"

def read_docx(uploaded_file):
    uploaded_file.seek(0)
    file_bytes = BytesIO(uploaded_file.read())
    return docx2txt.process(file_bytes)

def read_pdf(uploaded_file):
    uploaded_file.seek(0)
    reader = PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def clean_extracted_text(text):
    lines = text.splitlines() # Split into lines
    cleaned_lines = [line.strip() for line in lines if line.strip()]  # Remove empty lines and trim whitespace
    return ' '.join(cleaned_lines)

def parse_resume(file):
    template = PromptTemplate(
        input_variables=["resume_text"],
        template="""
            Extract the following information from the resume text:
            - Full Name
            - Email
            - Phone Number
            - Location
            - Years of Experience (must be an integer)
            - Skills (simple list of all the skills)
            - Education (always return array of objects with each object representing (degree, institution, year: integer, gpa) for each educational qualification)
            Return the result as JSON.
            Resume Text:
            {resume_text}
            """)
    llm = ChatOpenAI(temperature=0, model_name="gpt-4.1-mini")
    chain = template | llm

    extracted_text = read_file(file)
    resume_text = clean_extracted_text(extracted_text)

    structured_response = chain.invoke({"resume_text": resume_text})

    # removing extra characters from the response
    structured_response = str(structured_response.content).replace("```", "").replace("json", "")

    return structured_response

def shortlisting(candidates, education, skills ):
    similarity_threshold=0.7
    model = SentenceTransformer("all-MiniLM-L6-v2")

    template = PromptTemplate(
        input_variables=["required_skills"],
        template="""
            Extract all the required skills in a simple list in the following format:
            "skills": [ <array of all the extracted skills]
            Return the result as JSON.
            Required skills:
            {required_skills}
            """)
    llm = ChatOpenAI(temperature=0, model_name="gpt-4.1-mini")
    chain = template | llm

    structured_response = chain.invoke({"required_skills": skills})

    # removing extra characters from the response
    structured_response = str(structured_response.content).replace("```", "").replace("json", "")

    structured_response = json.loads(structured_response)

    required_skills = structured_response['skills']

    # Embed required skills
    required_Sembeddings = model.encode(required_skills, convert_to_tensor=True)
    required_Eembeddings = model.encode(education, convert_to_tensor=True)

    results = {}
    results['scores'] = {}

    for candidate in candidates:

        # --- Skills Scoring ---
        candidate_skills = candidate["skills"][:] 
        candidate_embeddings = model.encode(candidate_skills, convert_to_tensor=True)

        score = 0
        matched_indices = set()

        for req_idx, req_emb in enumerate(required_Sembeddings):
            for cand_idx, cand_emb in enumerate(candidate_embeddings):
                if cand_idx in matched_indices:
                    continue
                similarity = util.cos_sim(req_emb, cand_emb).item()
                if similarity >= similarity_threshold:
                    score += 1
                    matched_indices.add(cand_idx)
                    break  # go to next required skill
        
        # --- Education Scoring ---

        candidate_education = candidate['education'] 
        candidate_edu_embeddings = model.encode(candidate_education, convert_to_tensor=True)

        max_edu_similarity = 0
        for cand_edu_emb in candidate_edu_embeddings:
            similarity = util.cos_sim(required_Eembeddings, cand_edu_emb).item()
            max_edu_similarity = max(max_edu_similarity, similarity)

        results['scores'][candidate['username']] = {
            'skill_score': score,
            'education_similarity': max_edu_similarity
        }
    results['required_skills'] = required_skills

    return results

 




