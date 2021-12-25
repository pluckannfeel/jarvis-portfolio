from django import forms
from .models import Contact
from django.core.exceptions import ValidationError

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = [
            'name', 
            'subject',
            'email',
            'message'
        ]
        
        labels = {
            "name": "Name",
            "subject": "Subject",
            "email": "Email Address",
            "message": "Message"
        }
        
        widgets = {
            'name': forms.TextInput(attrs={'class': 'contact_input', 'required': True, 'id': 'contact_form_name'}),
            'subject': forms.TextInput(attrs={'class': 'contact_input', 'required': True, 'id': 'contact_form_subject'}),
            'email': forms.TextInput(attrs={'class': 'contact_input', 'required': True, 'id': 'contact_form_email'}),
            'message': forms.Textarea(attrs={'class': 'contact_input', 'cols': '0', 'rows': '7', 'required': True, 'id': 'contact_form_message'}),
        }
        
        def clean_name(self):
            name = self.cleaned_data.get('name')
            return name
        
        def clean_subject(self):
            name = self.cleaned_data.get('name')
            return name
        
        def clean_email(self):
            email = self.cleaned_data.get('email')
            return email
        
        def clean_message(self):
            message = self.cleaned_data.get('message')
            return message