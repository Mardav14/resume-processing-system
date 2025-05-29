from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('', views.getRoutes),
    path('shortlist', views.shortlist),
    path('resume/<str:username>', views.download_resume, name='download_resume'),
    path('candidate/<str:username>', views.candidate, name='download_resume'),

    path('token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.registerUser , name='registerUser'),
    path('registerHr/', views.registerUserHr , name='registerUserHr'),
]