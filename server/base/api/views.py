from django.http import JsonResponse, FileResponse, Http404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from .serializers import UserSerializer, EducationSerializer, SkillSetsSerializer
from base.models import Education, SkillSets
from django.contrib.auth import get_user_model
from . import resume_processor
import json
import os
from django.shortcuts import get_object_or_404
import mimetypes

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
    data = request.data.copy()  # Make mutable copy

    document = request.FILES.get('resume') 

    if document:
        parsed_info = resume_processor.parse_resume(document)
        print(parsed_info)
        parsed_info = json.loads(parsed_info)

        document.name = f"{data['username']}_{document.name}"
        data['full_name'] = parsed_info['Full Name']
        data['email'] = parsed_info['Email']
        data['phone'] = parsed_info['Phone Number']
        data['location'] = parsed_info['Location']
        data['years_experience'] = parsed_info['Years of Experience']
        data['resume'] = document
        

    skillSets = {
    'username': data.get('username'),
    'skills': parsed_info['Skills'],
    }
    
    education_data = parsed_info["Education"]
    
    educationList = []

    for entry in education_data:
        education_serializer = EducationSerializer(data={
            "username": data.get("username"),
            "degree": entry.get("degree", ""),
            "institution": entry.get("institution", ""),
            "year": entry.get("year", 0),
            "gpa": entry.get("gpa", "")
        })
        educationList.append(entry.get("degree"))
        
        if education_serializer.is_valid():
            education_serializer.save()

        else:
            print("something went wrong")    


    data['education_list'] = json.dumps(educationList)

    serializerU = UserSerializer(data=data)
    serializerS = SkillSetsSerializer(data=skillSets)
    
    if serializerU.is_valid() and serializerS.is_valid():
        serializerU.save()
        serializerS.save()
        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
    print(serializerU.errors)
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def registerUserHr(request):
    
    serializerU = UserSerializer(data=request.data)
    
    if serializerU.is_valid():
        serializerU.save()
        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
    print(serializerU.errors)
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def shortlist(request):
    filtered_candidates = []

    candidates = SkillSets.objects.all()
    min_years_experience = int(request.data.get('years_experience'))
    required_skills = request.data.get('required_skills')
    required_education = request.data.get('required_education')

    for candidate in candidates:
        try:
            curr_user = User.objects.get(username=candidate.username)
            if curr_user.years_experience is not None and curr_user.years_experience >= min_years_experience and curr_user.is_hr == False:
                newCandidate = {
                    'username': candidate.username,
                    'skills': candidate.skills,
                    'education': curr_user.education_list
                }
                filtered_candidates.append(newCandidate)
        except User.DoesNotExist:
            continue  
    print(filtered_candidates)
    result = resume_processor.shortlisting(
        filtered_candidates,
        required_education,
        required_skills
    )
    
    return Response(result, status=status.HTTP_200_OK)

@api_view(['GET'])
def download_resume(request, username):
    user = get_object_or_404(User, username=username)
    resume_file = user.resume 

    if not resume_file:
        raise Http404("Resume not found")

    filepath = resume_file.path
    filename = os.path.basename(filepath)

    # Detect MIME type
    mime_type, _ = mimetypes.guess_type(filepath)
    if not mime_type:
        mime_type = 'application/octet-stream'

    response = FileResponse(open(filepath, 'rb'), content_type=mime_type)
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response

@api_view(['GET'])
def candidate(request, username):
    user = get_object_or_404(User, username=username)
    skills_obj = get_object_or_404(SkillSets, username=username)
    
    serializer = UserSerializer(user)
    user_data = serializer.data
    user_data['skills'] = skills_obj.skills
    
    return Response(user_data, status=status.HTTP_200_OK)