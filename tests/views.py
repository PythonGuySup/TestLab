from django.shortcuts import render
from .models import Test, Question, Answer

def test_detail(request, test_id):
    test = Test.objects.get(pk=test_id)
    return render(request, 'test_detail.html', {'test': test})


def test_questions(request, test_id):
    test = Test.objects.get(id=test_id)
    questions = Question.objects.filter(test=test)
    answers = Answer.objects.filter(question__in=questions)

    context = {
        'test': test,
        'questions': questions,
        'answers': answers
    }

    return render(request, 'test_questions.html', context)
