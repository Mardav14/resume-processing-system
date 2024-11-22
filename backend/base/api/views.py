from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from .serializers import UserSerializer, JobSerialiser
from base.models import Job
from django.contrib.auth import get_user_model
from . import chatGpt
import json
User = get_user_model()


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['is_hr'] = user.is_hr
        # ...

        return token
    
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class= MyTokenObtainPairSerializer

@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/api/token',
        '/api/token/refresh',
        '/api/register',
        '/api/jobs',
        '/api/questions',
    ]

    return Response(routes)

@api_view(['POST'])
def registerUser(request):
    serializer = UserSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def getJobsAll(request):
    jobs = Job.objects.all()
    serialized_data = []

    for job in jobs:
        serializer = JobSerialiser(job)
        serialized_data.append(serializer.data)

    return Response(serialized_data)

@api_view(['POST'])
def getJobs(request):
    data = json.loads(request.body)
    company = data.get('company')
    
    jobs = Job.objects.filter(company = company)
    serialized_data = []
    for job in jobs:
        serializer = JobSerialiser(job)
        serialized_data.append(serializer.data)

    return Response(serialized_data)

@api_view(['POST'])
def getQuestions(request):
    data = json.loads(request.body)
    username = data.get('username')
    url = data.get('url')
    test_data = Job.objects.get(url=url)
    user = User.objects.get(username = username)
    serializer = JobSerialiser(test_data)
    desc = test_data.desc
    resume = user.resume.path
    resume_text = chatGpt.read_file(resume)
    questions =chatGpt.get_all_questions(desc, resume_text)
    # serialized_data = {**serializer.data, 'questions': ['Hello, Mardav', 'Tell us something about yourself.', 'What is the importance of resourcefulness in a fast-paced and innovative work environment?', 'What is the key characteristic of a person with resourcefulness?', 'Which skill involves the ability to measure initiatives quantitatively and draw actionable insights to guide decisions?', 'Can you provide an example of a time when you demonstrated resourcefulness in a work setting?', 'Can you provide an example of a project where you demonstrated resourcefulness and worked effectively with a lean team to achieve successful results?', 'Can you provide an example of a project where you demonstrated resourcefulness and worked effectively with a lean team to achieve successful outcomes?']}
    serialized_data = {**serializer.data, 'questions': questions}
    return Response(serialized_data)

@api_view(['POST'])
def createJob(request):
    serializer = JobSerialiser(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Job Opening created successfully'}, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def getScore(request):
    data = json.loads(request.body)
    username = data.get('username')
    print(data)
    url = data.get('url')
    print(url)
    test_data = Job.objects.get(url=url)
    user = User.objects.get(username = username)

    answers = chatGpt.get_all_answers(data.get('questions'), data.get('answers'))
    totalScore = int((answers[0]+ answers[1]+answers[2]+ answers[3]+ answers[4]+answers[5]+ answers[6]+ answers[7])*10)
    test_data.scores.append({"username": username, "score": totalScore, "email": user.email})
    test_data.scores.sort(key=lambda x: x.get('score', 0))
    test_data.save()
    return Response(answers)
    
# ["hi, mardav", "tell us about yourself", "importance of project a)a b)b","importance of project a)a b)b","importance of project a)a b)b","importance of project ","importance of project ","importance of project"]
# 'questions': ['Hello, Mardav', 'Tell us something about yourself.', 'What is the importance of resourcefulness in a fast-paced and innovative work environment?\n\nA) Resourcefulness helps in maintaining a structured project management approach.\nB) Resourcefulness allows for quick decision-making and problem-solving.\nC) Resourcefulness is primarily focused on individual achievements.', 'What is the key characteristic of a person with resourcefulness?\nA) Ability to manage multiple projects simultaneously\nB) Capability to find solutions with limited resources\nC) Strong communication skills\nD) Proficiency in programming languages', 'Which skill involves the ability to measure initiatives quantitatively and draw actionable insights to guide decisions?\n\nA) Project management skills  \nB) Analytical abilities  \nC) Ability to work with remote teams  \nD) Resourcefulness  \nE) Experience working with lean teams  ', 'Can you provide an example of a time when you demonstrated resourcefulness in a work setting?', 'Can you provide an example of a project where you demonstrated resourcefulness and worked effectively with a lean team to achieve successful results?', 'Can you provide an example of a project where you demonstrated resourcefulness and worked effectively with a lean team to achieve successful outcomes?']}
