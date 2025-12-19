from django.db import models
from django.contrib.auth.models import AbstractUser

class Mahasiswa(AbstractUser):
    # Default fields: username, email, first_name, last_name, password
    email = models.EmailField(unique=True) 
    prodi = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)
    foto_profil = models.ImageField(upload_to='profiles/', blank=True, null=True)
    is_active_talent = models.BooleanField(default=False) 

    USERNAME_FIELD = 'email' 
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='mahasiswa_set', # related_name unik
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='mahasiswa_permissions_set', 
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )
    

class Skill(models.Model):
    mahasiswa = models.ForeignKey(Mahasiswa, on_delete=models.CASCADE, related_name='skills')
    nama_skill = models.CharField(max_length=100)
    level = models.IntegerField(default=1) # 1-5 atau skala lain

    def __str__(self):
        return f"{self.nama_skill} ({self.mahasiswa.email})"
    
class Experience(models.Model):
    mahasiswa = models.ForeignKey(Mahasiswa, on_delete=models.CASCADE, related_name='experiences')
    judul = models.CharField(max_length=255)
    perusahaan = models.CharField(max_length=255, blank=True)
    deskripsi = models.TextField(blank=True)
    tanggal_mulai = models.DateField()
    tanggal_selesai = models.DateField(null=True, blank=True) # Bisa null jika masih bekerja

    def __str__(self):
        return self.judul
    
class Portfolio(models.Model):
    mahasiswa = models.ForeignKey(Mahasiswa, on_delete=models.CASCADE, related_name='portfolios')
    judul = models.CharField(max_length=255)
    deskripsi = models.TextField()
    url_proyek = models.URLField(blank=True)
    # file_media = models.FileField(...)

    def __str__(self):
        return self.judul