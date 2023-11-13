from django.db import models
from django.contrib.auth.models import User

class Certificate(models.Model):
    name = models.CharField(max_length=100)
    organization = models.CharField(max_length=100)
    certificate_for = models.CharField(max_length=100)
    assigned_date = models.DateField()
    expire_date = models.DateField()
    email = models.EmailField()
    certificate_id = models.CharField(max_length=64, blank=True, null=True)

    def __str__(self):
        return self.email

class Organization(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    website = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}'s Organization"

class PDFModel(models.Model):
    title = models.CharField(max_length=80)
    pdf = models.FileField(upload_to='pdfs/')

    def __str__(self):
        return self.title
