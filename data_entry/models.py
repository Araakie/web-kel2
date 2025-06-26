from django.db import models
from django import forms
from datetime import date




# Create your models here.
class Pengguna (models.Model):
    email = models.EmailField()
    password = models.CharField(max_length=100)
    address_1 = models.TextField()
    address_2  = models.TextField(null=True, blank = True)
    city = models.CharField(max_length=20, help_text='Enter your city')
    state= models.TextField()
    zip_code= models.CharField(max_length = 7)
    tanggal_join = models.DateField(auto_now = True)

    def __str__(self):
     return f'{self.email}'

from django.db import models

class Unit(models.Model):
    nama = models.CharField(max_length=100)

    def __str__(self):
        return self.nama

from django.db import models

class ParameterOptPembebanan(models.Model):
    nama = models.CharField(max_length=100)
    nilai = models.FloatField()

class ParameterBlending(models.Model):
    bahan = models.CharField(max_length=100)
    proporsi = models.DecimalField(max_digits=5, decimal_places=2)

class Content(models.Model):
    author = models.ForeignKey(Pengguna, on_delete=models.CASCADE)
    date_created = models.DateField(auto_now=True)
    artikel = models.TextField()
    set_view = models.BooleanField(default=False)

from django.db import models


class Project(models.Model):
    nama = models.CharField(max_length=100)
    deskripsi = models.TextField()
    mulai = models.DateField()
    selesai = models.DateField()
    penanggungjawab = models.CharField(max_length=100)
    jumlah = models.IntegerField()
    file = models.FileField(upload_to='uploads/', null=True, blank=True)
    pendanaan = models.BigIntegerField(null=True, blank=True)
    aktivitas1 = models.CharField(max_length=100, null=True, blank=True)
    aktivitas2 = models.CharField(max_length=100, null=True, blank=True)
    aktivitas3 = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.nama

    
from django.db import models

class Timeline(models.Model):
    nama = models.CharField(max_length=100)
    deskripsi = models.TextField(blank=True, null=True)  # ← pastikan ada ini
    status = models.IntegerField()
    file_pdf = models.FileField(upload_to='file_pdfs/', blank=True, null=True)


    def __str__(self):
        return self.nama


from django.db import models

class Profile(models.Model):
    nama = models.CharField(max_length=100)
    alamat = models.CharField(max_length=255)
    tgl_lahir = models.DateField()
    telp = models.CharField(max_length=15)
    foto = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

    def __str__(self):
        return self.nama
    
class Management(models.Model):
    namaKelompok = models.TextField()
    deskripsi = models.TextField()
    status = models.TextField()

    def _str_(self):
        return f"{self.namaKelompok} - {self.status}"
    
from django.db import models

class ProjectManagement(models.Model):
    nama_kelompok = models.CharField(max_length=100)
    nama_model = models.CharField(max_length=100, default="default_model")
    status_model = models.CharField(max_length=100)
    deskripsi_model = models.TextField(null=True, blank=True)
    file = models.FileField(upload_to='uploaded_files/', null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nama_model
    

class ModelMasuk(models.Model):
    nama_kelompok = models.CharField(max_length=100)
    deskripsi = models.TextField()
    status = models.CharField(max_length=100)

    def __str__(self):
        return self.nama_kelompok


    




