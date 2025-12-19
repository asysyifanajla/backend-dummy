from django.contrib import admin
from .models import Mahasiswa, Skill, Experience, Portfolio

@admin.register(Mahasiswa)
class MahasiswaAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'prodi', 'is_active_talent')
    list_filter = ('is_active_talent', 'prodi')
    search_fields = ('email', 'username')

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('nama_skill', 'level', 'mahasiswa')

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('judul', 'perusahaan', 'mahasiswa')

@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('judul', 'mahasiswa')
