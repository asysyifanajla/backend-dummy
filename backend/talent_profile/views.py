from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, generics
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from .models import Skill, Experience, Portfolio, Mahasiswa
from .serializers import (
    RegisterSerializer, 
    MahasiswaProfileSerializer,
    SkillSerializer,
    ExperienceSerializer,
    PortfolioSerializer 
)
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import MyTokenObtainPairSerializer

from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

from .models import Mahasiswa
# Public Talent API endpoints

# --- 1. Endpoint Register 
class RegisterView(APIView):
    permission_classes = () 

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# --- 2. Endpoint Mahasiswa Profile
class MyProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,) 
    serializer_class = MahasiswaProfileSerializer

    def get_object(self):
        return self.request.user


# --- 3. ViewSets for CRUD Skill, Experience, dan Portfolio ---

class BaseUserItemViewSet(viewsets.ModelViewSet):
    """Base ViewSet untuk item yang dimiliki user (Skill, Experience, Portfolio)"""
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(mahasiswa=self.request.user)

    def perform_create(self, serializer):
        serializer.save(mahasiswa=self.request.user)

# --- 4. endpoint Login
# class LoginView(APIView):
#     authentication_classes = []
#     permission_classes = []

#     def post(self, request):
#         username = request.data.get("email")
#         password = request.data.get("password")

#         if not username or not password:
#             return Response(
#                 {"detail": "email dan password wajib"},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         user = authenticate(email=email, password=password)

#         if user is None:
#             return Response(
#                 {"detail": "email atau password salah"},
#                 status=status.HTTP_401_UNAUTHORIZED
#             )

#         refresh = RefreshToken.for_user(user)

#         return Response({
#             "access": str(refresh.access_token),
#             "refresh": str(refresh),
#         })

class LoginView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    
# CRUD for Skill
class SkillViewSet(BaseUserItemViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [IsAuthenticated]


# CRUD for Experience
class ExperienceViewSet(BaseUserItemViewSet):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer
    


# CRUD for Portfolio
class PortfolioViewSet(BaseUserItemViewSet):
    queryset = Portfolio.objects.all()
    serializer_class = PortfolioSerializer


# --- 4. Public Talent API (untuk pengunjung) ---

class PublicTalentListView(ListAPIView):
    serializer_class = MahasiswaProfileSerializer
    permission_classes = []  # publik, tidak perlu login

    def get_queryset(self):
        qs = Mahasiswa.objects.filter(is_active_talent=True)

        search = self.request.query_params.get('search')
        prodi = self.request.query_params.get('prodi')
        skill = self.request.query_params.get('skill')

        if search:
            qs = qs.filter(username__icontains=search)

        if prodi:
            qs = qs.filter(prodi__icontains=prodi)

        if skill:
            qs = qs.filter(skills__nama_skill__icontains=skill)

        return qs.distinct()


class PublicTalentDetailView(RetrieveAPIView):
    queryset = Mahasiswa.objects.filter(is_active_talent=True)
    serializer_class = MahasiswaProfileSerializer
    permission_classes = []  # publik


class LatestTalentView(ListAPIView):
    serializer_class = MahasiswaProfileSerializer
    permission_classes = []

    def get_queryset(self):
        return Mahasiswa.objects.filter(is_active_talent=True).order_by('-date_joined')[:5]

# --- 5. Download CV as PDF ---
class DownloadCVView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        mahasiswa = request.user

        template = get_template('cv/cv_template.html')
        html = template.render({
            'mahasiswa': mahasiswa,
            'skills': mahasiswa.skills.all(),
            'experiences': mahasiswa.experiences.all(),
            'portfolios': mahasiswa.portfolios.all(),
        })

        response = HttpResponse(content_type='application/pdf')
        filename = f"cv-{mahasiswa.username}.pdf"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        pisa_status = pisa.CreatePDF(
            html,
            dest=response,
            encoding='UTF-8'
        )

        if pisa_status.err:
            return HttpResponse("Gagal generate PDF", status=500)

        return response