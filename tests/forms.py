from django import forms
import tests.models


class ValidTest(forms.Form):
    category = forms.CharField(max_length=50)
    time = forms.TimeField()
    title = forms.CharField(max_length=60)
    description = forms.CharField(max_length=255)
    author = forms.CharField()
    questions = forms.CharField()    


class ValidQuestion(forms.Form):
    question = forms.CharField(max_length=255)
    multiple_ans = forms.BooleanField()
    answers = forms.CharField()
    
