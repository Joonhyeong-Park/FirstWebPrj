from django import forms
from django.forms import ModelChoiceField
from .models import Message, Report
from accounts.models import MyUser

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
        widgets = {
            'content': forms.Textarea(
                attrs = {
                    'class': 'form-control',
                    'placeholder': '메세지를 작성해주세요',
                }
            )
        }

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['user','report1','report2','report3','content']