import openai
# from docx import Document
import docx2txt
import PyPDF2
import tiktoken
import mimetypes
import random

# OpenAI API key
# openai.api_key = "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"


# File paths


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

# Main function
def main():
    resume = read_file(resume_file_path)
    job_description = read_file(job_description_file_path)
    interview_chatbot(job_description, resume)

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

# Getting how the candidate greets
# def ask_greeting(candidate_name):
#     return("Hello, " + candidate_name)

    
# def ask_greeting_ans(conversation, reply):
#     conversation.append({"role": "user", "content": "Candidate has greeted to the interviewer in the following manner: " + reply + "\n\n\nIf the greeting was polite and professional and didn't have any spelling error or grammar error, then JUST WRITE 1 IN THE CHATBOX, ELSE WRITE JUST 0 IN THE CHATBOX"})
#     return int(ask_chatgpt(conversation, max_no_of_tokens_for_getting_scores, temp_for_getting_scores, top_p_for_getting_scores, frequency_penalty_for_getting_scores))

# Getting the proper introduction
def ask_introduction(name):
    question = f"Hello {name}, Tell us something about yourself."
    return question
    
def ask_introduction_ans(candidate_name, conversation, reply):
    conversation.append({"role": "user", "content": "WRITE THE ANSWER IN ONE NUMBER ONLY. This is the intro that the candidate gave of himself: " + reply + "This is his name: " + candidate_name + "\n\n\nThe intro should contain all six things: 1.name, 2.place of birth and place where he was brought up, 3.Details of latest education (year of graduation, course, college), 4. Skills given by candidate, 5. family backround, 6.hobbies. IF EACH CRITERIA IS MET, WRITE 1. ELSE WRITE 0"})
    reply = ask_chatgpt(conversation, max_no_of_tokens_for_getting_scores, temp_for_getting_scores, top_p_for_getting_scores, frequency_penalty_for_getting_scores)
    return float(reply) / 2

# Getting the skills that the person has
def get_candidate_skills(conversation):
    conversation.append({"role": "user", "content": "Please find out all the technical skills that this person has"})
    return ask_chatgpt(conversation)

# Getting the skills that are absolutely required
def get_required_skills(conversation):
    conversation.append({"role": "user", "content": "Please find all the technical skills that are absolutely required in this job according to the job description. Ignore the resume for now. Leave out all the skills that are not so required"})
    return ask_chatgpt(conversation)

# Getting the skills that are optional in the job
def get_optional_skills(conversation):
    conversation.append({"role": "user", "content": "Please find all the optional skills from the job description that are just good to have. Ignore the resume for now"})
    return ask_chatgpt(conversation)

# Getting all the experiences
def get_experience_of_candidate(conversation):
    conversation.append({"role": "user", "content": "Please list out all the experience and the work done by the candidate. Include the organization name and the duration of work."})
    return ask_chatgpt(conversation)

# Getting the matched skills
def get_matched_skills(conversation, skills_required, skills_of_candidate, experience_of_candidate):
    conversation.append({"role": "user", "content": "Please find all the skills that matched based on the following. Skills required: " + skills_required + "\n\n\nSkills available with the candidate: " + skills_of_candidate + "\n\n\nExperience of candidate: " + experience_of_candidate})
    return ask_chatgpt(conversation)

# Getting matched optional skills
def get_matched_optional_skills(conversation, optional_skills, skills_of_candidate, experience_of_candidate):
    conversation.append({"role": "user", "content": "Please find all the optional skills that are found in the skills or experiences of the candidate's resume. Optional skills required: " + optional_skills + "\n\n\nSkills of candidate: " + skills_of_candidate + "\n\n\nExperiences of candidate: " + experience_of_candidate})
    return ask_chatgpt(conversation)

# Asking some skill questions
def ask_skill_question(conversation, skills_required):
    
    conversation.append({"role": "user", "content": "Here are some skills that we need: " + skills_required})
    
    conversation.append({"role": "user", "content": "Ask me a question related to one of the skills above. don't give any instructions. the question should be different from ALL the questions asked before in the conversation"})
    question = ask_chatgpt(conversation)
    return question
def ask_questions(name, conversation, skills_required):
    
    conversation.append({"role": "user", "content": "Here are some skills that we need: " + skills_required})
    
    conversation.append({"role": "user", "content": f"give 8 questions based on the provided skills. only respond with questions and nothing else. first question should always be introduce yourself beginning with a greeting with candidate's name which is {name}. separate each question by a ';'. don't give any instructions."})
    question = ask_chatgpt(conversation)
    return question
    

def ask_skill_question_ans(question, reply):
    skillpoints = 0
    qna = [{"role": "user", "content": "Here is a question: " + question + "Here is the answer: " + reply + "IF THE ANSWER IS CORRECT, WRITE 1, ELSE WRITE 0, DONT WRITE ANYTHING ELSE"}]
        # conversation.append({"role": "user", "content" : "JUST WRITE '7'"}) #. Here is your question: " + question + "\n\nHere is the user's reply to your question: " + reply + "\n\n\nIF THE ANSWER IS CORRECT, WRITE 1. IF THE ANSWER IS WRONG, WRITE 0"})
    reply = ask_chatgpt(qna, max_no_of_tokens_for_getting_scores, temp_for_getting_scores, top_p_for_getting_scores, frequency_penalty_for_getting_scores)
    try:
        skillpoints = skillpoints + int(reply)
    except ValueError:

        skillpoints = skillpoints + random.randint(0, 1)
    return skillpoints


# Asking some experience question
def ask_experience_question(conversation, experience_of_candidate):
    
    conversation.append({"role": "user", "content": "Here are the experiences of the candidate: " + experience_of_candidate})
    
    conversation.append({"role": "user", "content": "Ask me a question related to one of the experiences above. Question should be such that it expects descriptive answers. (e.g. explain did you manage this project?). Don't give any instructions. the question should be different from ALL the questions asked before in the conversation"})
    question = ask_chatgpt(conversation)
    # conversation.append({"role" : "assistant", "content": question})
    return (question)

def ask_experience_question_ans(question, reply): 
    experience_points = 0
    # conversation.append({"role": "user", "content" : "WRITE ANY NUMBER"})#. Here is your question: " + question + "Here is the user's reply to your question: " + reply + "\n\n\nIf in the reply he shared an experience, WRITE 1, else WRITE 0"})
    qna = [{"role": "user", "content": "Here is a question: " + question + "Here is the answer: " + reply + "IF THE ANSWER CONTAINS WORDS RELATED TO LEADERSHIP (E.G. lead, Chief, head, ETC.), WRITE 1, ELSE WRITE 0"}]
    reply = ask_chatgpt(qna, max_no_of_tokens_for_getting_scores, temp_for_getting_scores, top_p_for_getting_scores, frequency_penalty_for_getting_scores)
    try:
        experience_points = experience_points + int(reply)
    except ValueError:
        experience_points = experience_points + random.randint(0, 1)
    return experience_points



# Starting the interview
def interview_chatbot(job_description, resume):
    # Initialize conversation with job description         
    conversation = [
        {"role": "system", "content": "You are a person who is supposed to take interviews of candidates based on the resume and job description."},
        {"role": "user", "content": "Here is the job description: " + job_description},
        {"role": "user", "content": "Here is the candidate's resume: " + resume}
    ]

    candidate_name = get_name(conversation)
    skills_required = get_required_skills(conversation)
    optional_skills = get_optional_skills(conversation)
    experience_of_candidate = get_experience_of_candidate(conversation)
    skills_of_candidate = get_candidate_skills(conversation)
    matched_skills = get_matched_skills(conversation,  skills_required, skills_of_candidate, experience_of_candidate)
    matched_optional_skills = get_matched_optional_skills(conversation, optional_skills, skills_of_candidate, experience_of_candidate)
    greeting_points = ask_greeting(conversation, candidate_name) * correct_answer_points
    introduction_points = ask_introduction(conversation, candidate_name) * correct_answer_points
    skillpoints = ask_skill_question(conversation, skills_required) * correct_answer_points
    experience_points = ask_experience_question(conversation, experience_of_candidate) * correct_answer_points

    

    candidate_details = {
        "Name": candidate_name,
        "Experience": experience_of_candidate,
        "Skills": skills_of_candidate,
        "Matched Skills": matched_skills,
        "Matched Optional Skills": matched_optional_skills,
        "Greeting points": greeting_points,
        "Introduction points": introduction_points,
        "Skill points": skillpoints,
        "Experience points": experience_points,
        "Overall points": greeting_points + introduction_points + skillpoints + experience_points
    }

    print("Greeting points: " + str(candidate_details["Greeting points"]))
    print("Introduction points: " + str(candidate_details["Introduction points"]))
    print("Skill points: " + str(candidate_details["Skill points"]))
    print("Experience points: " + str(candidate_details["Experience points"]))
    print("Overall points: " + str(candidate_details["Overall points"]))

    


# Starting with the interview
# if __name__ == "__main__":
#     main()

def get_all_questions(job_description, resume):
    allQuestions = []
    conversation = [
        {"role": "system", "content": "You are a person who is supposed to take interviews of candidates based on the resume and job description."},
        {"role": "user", "content": "Here is the job description: " + job_description},
        {"role": "user", "content": "Here is the candidate's resume: " + resume}
    ]

    candidate_name = get_name(conversation)
    skills_required = get_required_skills(conversation)
    # optional_skills = get_optional_skills(conversation)
    # experience_of_candidate = get_experience_of_candidate(conversation)
    # skills_of_candidate = get_candidate_skills(conversation)
    # matched_skills = get_matched_skills(conversation,  skills_required, skills_of_candidate, experience_of_candidate)
    # matched_optional_skills = get_matched_optional_skills(conversation, optional_skills, skills_of_candidate, experience_of_candidate)

    # allQuestions.append(ask_greeting(candidate_name))
    combined_questions = ask_questions(candidate_name, conversation, skills_required)
    questions = combined_questions.split("\n")
    print(questions)
    # allQuestions.append(ask_introduction(candidate_name, conversation, skills_required))

    # for _ in range(3):
    #     allQuestions.append(ask_skill_question(conversation, skills_required))

    # for _ in range(3):
    #     allQuestions.append(ask_experience_question(conversation, skills_required))

    return questions

def get_all_answers(job_description, resume, questions, answers):
    allScores = []
    conversation = [
        {"role": "system", "content": "You are a person who is supposed to take interviews of candidates based on the resume and job description."},
        {"role": "user", "content": "Here is the job description: " + job_description},
        {"role": "user", "content": "Here is the candidate's resume: " + resume}
    ]

    candidate_name = get_name(conversation)
    skills_required = get_required_skills(conversation)
    optional_skills = get_optional_skills(conversation)
    experience_of_candidate = get_experience_of_candidate(conversation)
    skills_of_candidate = get_candidate_skills(conversation)
    matched_skills = get_matched_skills(conversation,  skills_required, skills_of_candidate, experience_of_candidate)
    matched_optional_skills = get_matched_optional_skills(conversation, optional_skills, skills_of_candidate, experience_of_candidate)

    # allScores.append(ask_greeting_ans(conversation, answers[0]))
    allScores.append(ask_introduction_ans(candidate_name, conversation, answers[0]))
    for i in range(3):
        allScores.append(ask_skill_question_ans(questions[1+i], answers[1+i]))
    for i in range(3):
        allScores.append(ask_experience_question_ans(questions[4+i], answers[4+i]))
    
    return allScores
    
# get_all_questions()




