# AI Resume Parser & Candidate Shortlisting Tool

An AI-powered resume parser and shortlisting system built using **Django**, **React**, **LangChain with OpenAI**, and **Sentence Transformers**. It parses uploaded resumes, compares candidate skills and education against job requirements, and ranks candidates with smart shortlisting logic.

---

## Features

- 🔍 Resume parsing using OpenAI via LangChain
- 🤖 Skill and education similarity scoring using Sentence Transformers
- 📥 Resume upload and download functionality
- 📋 Detailed candidate view in modal
- 🧠 Ranked shortlisting based on requirements
- 🖥️ Interactive ReactJS + Bootstrap dashboard

### main code for resume processing is in "server/base/api/resume_processor.py" file
### main code for APIs is in "server/base/api/views.py" file
### main code for frontend dashboard is in "client/src/pages/HrDashboard.js" file

## Tech Stack

### Backend:
- Python, Django, Django REST Framework
- SQLite
- LangChain
- Sentence Transformers (SBERT)

### Frontend:
- ReactJS
- Bootstrap 5

## How to Run the Project Locally

### 1. Clone the Repository
### 2. Backend Setup
- cd backend
- pip install -r requirements.txt
- create .env
- add the API key
API_KEY=your_openai_api_key_here
- python manage.py makemigration
- python manage.py migrate
- python manage.py runserver

### 3. Frontend Setup
- cd ../client
- npm install
- npm start