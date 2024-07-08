from django import forms
from tests.models import Test, Question, Answer


class ValidTest(forms.ModelForm):
    class Meta:
        model = Test
        fields = ['time', 'title', 'description']

    questions = forms.JSONField()
    category = forms.CharField(max_length=50)


class ValidQuestion(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question', 'multiple_ans']

    answers = forms.JSONField()


class ValidAnswer(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['answer', 'right_answer']
