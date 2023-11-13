from django import forms
from .models import Certificate, PDFModel

class CertificateForm(forms.ModelForm):
    class Meta:
        model = Certificate
        fields = ['name', 'organization', 'certificate_for', 'assigned_date', 'expire_date', 'email']

def validate_pdf(value):
    if not value.name.endswith('.pdf'):
        raise ValidationError(_('Invalid file format. Only PDF files are allowed.'))

class UploadFileForm(forms.ModelForm):
    class Meta:
        model = PDFModel
        fields = ('title', 'pdf',)