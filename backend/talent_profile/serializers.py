from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import Mahasiswa, Skill, Experience, Portfolio # Import semua Model

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ('id', 'nama_skill', 'level')

class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = ('id', 'judul', 'perusahaan', 'deskripsi', 'tanggal_mulai', 'tanggal_selesai')

class PortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Portfolio
        fields = ('id', 'judul', 'deskripsi', 'url_proyek')

#Register ---

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )

    class Meta:
        model = Mahasiswa
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {
            'email': {'required': True}
        }

    def create(self, validated_data):
        user = Mahasiswa.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # Ambil input email dari JSON dan masukkan ke field username secara internal
        # 'initial_data' adalah data mentah yang dikirim user (misal: {"email": "..."})
        email = self.initial_data.get("email")
        password = self.initial_data.get("password")

        if email:
            attrs[self.username_field] = email
            
        return super().validate(attrs)
      
#Profil Mahasiswa

class MahasiswaProfileSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)
    experiences = ExperienceSerializer(many=True, read_only=True)
    portfolios = PortfolioSerializer(many=True, read_only=True)

    class Meta:
        model = Mahasiswa
        fields = (
            'id', 'email', 'username', 'prodi', 'bio', 'foto_profil', 
            'is_active_talent', 'skills', 'experiences', 'portfolios' # Tambahkan fields relasi
        )
        read_only_fields = ('email', 'username', 'is_active_talent')
