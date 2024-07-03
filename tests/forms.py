from django import forms
import tests.models


class ValidTest(forms.Form):
    category = forms.CharField(max_length=50)
    time = forms.TimeField()
    title = forms.CharField(max_length=60)
    description = forms.CharField(max_length=255)
    author = forms.CharField() # временное решение, потом будем получать из сеанса
    questions = forms.JSONField()    


class ValidQuestion(forms.Form):
    question = forms.CharField(max_length=255)
    multiple_ans = forms.BooleanField()
    answers = forms.JSONField()
    
    
class ValidAnswer(forms.Form):
    answer = forms.CharField(max_length=255)
    right_answer = forms.BooleanField()
    
