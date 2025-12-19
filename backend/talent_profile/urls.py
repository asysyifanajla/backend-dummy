from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter 
from .views import (
    RegisterView,
    LoginView,
    MyProfileView,
    SkillViewSet,      
    ExperienceViewSet, 
    PortfolioViewSet   
)
from .views import (
    PublicTalentListView,
    PublicTalentDetailView,
    LatestTalentView
)

from .views import DownloadCVView

router = DefaultRouter()
router.register(r'skills', SkillViewSet, basename='skill')
router.register(r'experiences', ExperienceViewSet, basename='experience')
router.register(r'portfolios', PortfolioViewSet, basename='portfolio')

urlpatterns = [
    path('auth/register', RegisterView.as_view(), name='register'),
    path('mahasiswa/profile/me', MyProfileView.as_view(), name='my-profile'),
    path('', include(router.urls)),
    path('talents', PublicTalentListView.as_view()),
    path('talents/latest', LatestTalentView.as_view()),
    path('talents/<int:pk>', PublicTalentDetailView.as_view()),
    path('profile/me', MyProfileView.as_view()),
    path('profile/me/download-cv', DownloadCVView.as_view(), name='download-cv'),
]
