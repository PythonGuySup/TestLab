from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Test, Question, Answer

def test_detail(request, test_id):
    test = Test.objects.get(pk=test_id)
    return render(request, 'test_detail.html', {'test': test})


def test_questions(request, test_id):
    test = Test.objects.get(id=test_id)
    questions_list = Question.objects.filter(test=test)
    paginator = Paginator(questions_list, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'test': test,
        'page_obj': page_obj
    }

    return render(request, 'test_questions.html', context)

