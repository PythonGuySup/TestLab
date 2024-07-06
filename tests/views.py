from django.core.paginator import Paginator
from django.shortcuts import render

from django.db import transaction
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError
from tests.forms import ValidTest, ValidQuestion, ValidAnswer
from tests.models import Test, Question, Category, User
from datetime import datetime
from json import JSONDecodeError, loads


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


def create_test(test):
    test.instance.category = Category.objects.get(name=test.cleaned_data['category'])
    user = test.cleaned_data['author']  # временное решение, потом будем получать из сеанса

    test.instance.author = User.objects.get(username=user)
    test.instance.created_at = datetime.now()
    test.instance.updated_at = test.instance.created_at

    test.save()


def create_question(question, test):
    question.instance.test = test
    question.save()


def create_answer(answer, question):
    answer.instance.question = question
    answer.save()


@transaction.atomic
def constructor_post(request):
    try:

        params_json = loads(request.body)

        test_form = ValidTest(params_json)

        if test_form.is_valid():

            create_test(test_form)

            for question_json in test_form.cleaned_data['questions'].values():

                question_form = ValidQuestion(question_json)

                if question_form.is_valid():

                    question = create_question(question_form, test_form.instance)
                    one_right = False
                    for answer_json in question_form.cleaned_data['answers'].values():
                        answer_form = ValidAnswer(answer_json)
                        if answer_form.is_valid():
                            one_right = one_right or answer_form.cleaned_data['right_answer']
                            create_answer(answer_form, question_form.instance)    

                        else:
                            transaction.set_rollback(True)
                            return HttpResponseBadRequest('invalid answer data:' + str(answer_json))
                    if not one_right:
                        transaction.set_rollback(True)
                        return HttpResponseBadRequest('At least one answer must be correct:' + str(question_form.cleaned_data['answers']))
                else:
                    transaction.set_rollback(True)
                    return HttpResponseBadRequest('invalid question data:' + str(question_json))
            
        else:
            transaction.set_rollback(True)
            return HttpResponseBadRequest('invalid test data:' + str(params_json))
        
        # transaction.set_rollback(True) # отключил транзакцию для тестов
        return HttpResponse("Test add sucsessfull")

    except JSONDecodeError:
        transaction.set_rollback(True)
        return HttpResponseBadRequest('invalid stream params to JSON: ' + str(request.body))
    
    except Exception as E:
        transaction.set_rollback(True)
        return HttpResponseServerError(E)


def constructor_get(resuest):
    return render(resuest, 'constructor.html')


# Create your views here.

def constructor(request):
    if request.method == 'POST':
        return constructor_post(request)
    elif request.method == 'GET':
        return constructor_get(request)

    # return render(request, 'get_tocken.html') получение токена для postman
