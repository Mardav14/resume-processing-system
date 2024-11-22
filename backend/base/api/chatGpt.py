import openai
# from docx import Document
import docx2txt
import PyPDF2
import tiktoken
import mimetypes
import random

# OpenAI API key
openai.api_key = "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"

# Some constants
interviewer = "Interviewer: "
interviewee = "You: "
correct_answer_points = 10
max_no_of_tokens_for_getting_scores = 1
temp_for_getting_scores = 1
top_p_for_getting_scores = 1
n_for_getting_scores = 1
frequency_penalty_for_getting_scores = 1
presence_penalty_for_getting_scores = 0
question_array = []

# Detecting filetype
def read_file(file_path):
    try:
        # Guess the MIME type based on file extension
        mime_type, _ = mimetypes.guess_type(file_path)

        if mime_type:
            return list_of_filetypes(mime_type, file_path)
        else:
            return "Unknown file type"

    except FileNotFoundError:
        return "File not found"

    except Exception as e:
        return f"Error: {str(e)}"

# List of file types
def list_of_filetypes(file_type, file_path):
    if(file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"):
        return read_docx(file_path)
    elif(file_type == "application/pdf"):
        return read_pdf(file_path)
    else:
        return "Wrong file type"
    
# Reading docx
def read_docx(file_path):
    text = docx2txt.process(file_path)
    return text

# Reading pdf
def read_pdf(file_path):
    pdfFileObj = open(file_path, 'rb')
    pdfReader = PyPDF2.PdfReader(pdfFileObj)
    pageObj = pdfReader.pages[0]
    filetext =  pageObj.extract_text()
    pdfFileObj.close()
    return filetext

# Asking chatgpt the query
def ask_chatgpt(conversation, setting_max_tokens = 150, setting_temp = 1.2, setting_top_p = 0.4, setting_frequency_penalty = 0.6):
    # Estimate the token count of the conversation
    conversation_text = " ".join([message["content"] for message in conversation])
    estimated_tokens = num_tokens_from_string(conversation_text)

    # Ensure that the estimated token count does not exceed the limit
    while estimated_tokens > 3000:
        # Remove the oldest message until the conversation fits within the token limit
        conversation.pop(0)
        conversation_text = " ".join([message["content"] for message in conversation])
        estimated_tokens = num_tokens_from_string(conversation_text)

    # Make the API call with the optimized conversation
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=conversation,
        max_tokens=setting_max_tokens,
        temperature=setting_temp,
        top_p=setting_top_p,
        n=1,
        frequency_penalty=setting_frequency_penalty,
        presence_penalty=0
    )
    reply = str(response.choices[0].message.content)
    return reply

# Number of tokens
def num_tokens_from_string(string: str, encoding_name="gpt-3.5-turbo") -> int:
    encoding = tiktoken.encoding_for_model(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

# Getting the name of the candidate
def get_name(conversation):
    conversation.append({"role" : "user", "content": "Please write just the first name"})
    return ask_chatgpt(conversation)

# Getting the skills that the person has
def get_candidate_skills(conversation):
    conversation.append({"role": "user", "content": "Please find out all the technical skills that this person has"})
    return ask_chatgpt(conversation)

# Getting the skills that are absolutely required
def get_required_skills(conversation):
    conversation.append({"role": "user", "content": "Please find all the technical skills that are absolutely required in this job according to the job description. Ignore the resume for now. Leave out all the skills that are not so required"})
    return ask_chatgpt(conversation)


# Getting all the experiences
def get_experience_of_candidate(conversation):
    conversation.append({"role": "user", "content": "Please list out all the experience and the work done by the candidate. Include the organization name and the duration of work."})
    return ask_chatgpt(conversation)


# Asking questions
def ask_questions(name, conversation, skills_required, experience_of_candidate):
    
    conversation.append({"role": "user", "content": "Here are some skills that we need: " + skills_required})
    conversation.append({"role": "user", "content": "This is the candidate's experience: " + experience_of_candidate})
    
    conversation.append({"role": "user", "content": f"give 8 questions based on the provided skills and the candidate's experience. only respond with questions and nothing else. first question should always be introduce yourself beginning with a greeting with candidate's name which is {name}. separate each question by a ';'. don't give any instructions."})
    question = ask_chatgpt(conversation)
    return question
    
#getting answers
def all_answers(question, reply):
    skillpoints = 0
    qna = [{"role": "user", "content": "Here is a question: " + question + "Here is the answer: " + reply + "IF THE ANSWER IS CORRECT OR SOUNDS IMPRESSIVE AND ON POINT, WRITE 1, ELSE WRITE 0, DONT WRITE ANYTHING ELSE"}]
        # conversation.append({"role": "user", "content" : "JUST WRITE '7'"}) #. Here is your question: " + question + "\n\nHere is the user's reply to your question: " + reply + "\n\n\nIF THE ANSWER IS CORRECT, WRITE 1. IF THE ANSWER IS WRONG, WRITE 0"})
    reply = ask_chatgpt(qna, max_no_of_tokens_for_getting_scores, temp_for_getting_scores, top_p_for_getting_scores, frequency_penalty_for_getting_scores)
    try:
        skillpoints = skillpoints + int(reply)
    except ValueError:

        skillpoints = skillpoints + random.randint(0, 1)
    return skillpoints

def get_all_questions(job_description, resume):

    conversation = [
        {"role": "system", "content": "You are a person who is supposed to take interviews of candidates based on the resume and job description."},
        {"role": "user", "content": "Here is the job description: " + job_description},
        {"role": "user", "content": "Here is the candidate's resume: " + resume}
    ]

    experience_of_candidate = get_experience_of_candidate(conversation)

    candidate_name = get_name(conversation)
    skills_required = get_required_skills(conversation)

    combined_questions = ask_questions(candidate_name, conversation, skills_required, experience_of_candidate)
    questions = combined_questions.split(";")
    print(questions)

    return questions

def get_all_answers(questions, answers):
    allScores = []   
    for i in range(8):
        allScores.append(all_answers(questions[i], answers[i]))
    
    
    return allScores
    




