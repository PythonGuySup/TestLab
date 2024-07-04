from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Test, Question, Answer

from django.db import transaction
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError
from tests.forms import ValidTest, ValidQuestion, ValidAnswer
from tests.models import Test, Question, Answer, Category, User
from datetime import datetime
import json


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


def create_test(test_form):
    test = Test()
    
    test.category = Category.objects.get(name=test_form.cleaned_data['category'])
    test.time = test_form.cleaned_data['time']
    test.title = test_form.cleaned_data['title']
    test.description = test_form.cleaned_data['description']
    user = test_form.cleaned_data['author'] # временное решение, потом будем получать из сеанса
    test.author = User.objects.get(username=user)
    test.created_at = datetime.now()
    test.updated_at = test.created_at
    
    test.save()
    
    return test
    
    
# Create your views here.
@transaction.atomic
def constructor(request):
    if request.method == 'POST':
        try:
            transaction.set_autocommit(False)
            
            try:
                params_json = json.loads(request.body)
            except:
                return HttpResponseBadRequest('invalid stream params to JSON: ' + str(request.POST))
            
            test_form = ValidTest(params_json)
            
            if test_form.is_valid():
                
                test = create_test(test_form)
                
                for question_json in test_form.cleaned_data['questions'].values():
                    
                    question_form = ValidQuestion(question_json)
                    
                    if question_form.is_valid():

                        for answer_json in question_form.cleaned_data['answers'].values():
                            answer_form = ValidAnswer(answer_json)
                            if answer_form.is_valid():
                                
                                pass    
                            
                            else:
                                transaction.set_rollback(True)
                                return HttpResponseBadRequest('invalid answer:' + str(answer_json))
                            
                    else:
                        transaction.set_rollback(True)
                        return HttpResponseBadRequest('invalid question:' + str(question_json))
                
            else:
                transaction.set_rollback(True)
                return HttpResponseBadRequest('invalid data:' + str(params_json))
            
            # transaction.commit() выключил для тестов
            transaction.set_autocommit(True)
            return HttpResponse("Test add sucsessfull")
        
        except Exception as E:
            transaction.set_rollback(True)
            return HttpResponseServerError(E)         
    
    # return render(request, 'get_tocken.html') получение токена для postman

