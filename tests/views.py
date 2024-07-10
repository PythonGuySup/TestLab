from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.db import transaction
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError
from tests.forms import ValidTest, ValidQuestion, ValidAnswer
from tests.models import Test, Question, Category, Answer
from datetime import datetime
from json import JSONDecodeError, loads

from tests.utils.flush_test_in_session import flush_test_in_session
from tests.utils.reformat_data import reformat_data
from tests.utils.update_session import update_session
from tests.utils.init_session import init_session
from django.template.defaulttags import register


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key).items()


def error_handler(request, exception):
    status_code = getattr(exception, 'status_code', 500)
    template_name = f"{status_code}.html"
    return render(request, template_name, status=status_code)


def test_detail(request, test_id):
    test = Test.objects.get(pk=test_id)
    return render(request, 'test_detail.html', {'test': test})


def test_questions(request, test_id):
    if request.method == 'POST':
        update_session(request, test_id)
        if request.POST.get('end') == '':
            return redirect('test_result', test_id)
    else:
        if not request.session.get(f'dict_{test_id}'.format(test_id=test_id), False):
            init_session(request, test_id)

    test = Test.objects.get(id=test_id)
    page_number = request.session['dict_{test_id}'.format(test_id=test_id)]['current_page']
    page_obj = request.session['dict_{test_id}'.format(test_id=test_id)]['page_{i}'.format(i=page_number)]
    page_obj = reformat_data(page_obj)
    has_next = False
    has_previous = False
    is_last_page = False

    if request.session['dict_{test_id}'.format(test_id=test_id)]['current_page'] < \
            request.session['dict_{test_id}'.format(test_id=test_id)]['pages']:
        has_next = True
    if request.session['dict_{test_id}'.format(test_id=test_id)]['current_page'] > 1:
        has_previous = True
    if page_number == request.session['dict_{test_id}'.format(test_id=test_id)]['pages']:
        is_last_page = True

    context = {
        'test': test,
        'page_obj': page_obj,
        'has_next': has_next,
        'has_previous': has_previous,
        "is_last_page": is_last_page
    }

    return render(request, 'test_questions.html', context)




def test_result(request, test_id):
    test = Test.objects.get(id=test_id)
    session_dict = request.session['dict_{test_id}'.format(test_id=test_id)]
    result = 0

    for i in range(1, session_dict['pages'] + 1):
        for question, answer_dict in session_dict['page_{i}'.format(i=i)].items():
            for answer, status in answer_dict.items():
                db_answer = Answer.objects.get(id=answer)
                if status:
                    if db_answer.right_answer:
                        result += 1

    flush_test_in_session(request, test.id)

    return render(request, 'test_result.html', {'test': test, 'result': result})


def create_test(test, test_id, user):
    test.instance.category, created = Category.objects.get_or_create(name=test.cleaned_data['category'])
    test.instance.author = user

    if test_id is None:
        test.instance.created_at = datetime.now()
    test.instance.updated_at = datetime.now()

    test.save()


def create_question(question, test):
    question.instance.test = test
    question.save()


def create_answer(answer, question):
    answer.instance.question = question
    answer.save()


def clear_questions(test_id):
    questions = Question.objects.filter(test=test_id).delete()


def rollback(message, details):
    transaction.set_rollback(True)
    return HttpResponseBadRequest(message + str(details))


@transaction.atomic
def constructor_post(request, test_id):

    try:

        params_json = loads(request.body)
        if Test.objects.filter(id=test_id).exists():
            test = Test.objects.get(id=test_id)

            if test.author != request.user:
                raise PermissionDenied

            test_form = ValidTest(params_json, instance=test)
        else:
            test_form = ValidTest(params_json)

        if test_form.is_valid():

            create_test(test_form, test_id, request.user)
            clear_questions(test_id)

            for question_json in test_form.cleaned_data['questions'].values():

                question_form = ValidQuestion(question_json)

                if question_form.is_valid():

                    create_question(question_form, test_form.instance)
                    count_right = 0
                    for answer_json in question_form.cleaned_data['answers'].values():
                        answer_form = ValidAnswer(answer_json)
                        if answer_form.is_valid():
                            if answer_form.cleaned_data['right_answer']:
                                count_right += 1
                            create_answer(answer_form, question_form.instance)
                        else:
                            return rollback('invalid answer data:', str(answer_json))

                    if not count_right:
                        return rollback(
                            'At least one answer must be correct:', str(question_form.cleaned_data['answers']))
                    elif question_form.cleaned_data['multiple_ans'] and count_right < 2:
                        return rollback(
                            'You must provide at least 2 correct answers:', str(question_form.cleaned_data['answers']))
                    elif not question_form.cleaned_data['multiple_ans'] and count_right >= 2:
                        return rollback(
                            'You must specify only 1 correct answer:', str(question_form.cleaned_data['answers']))
                else:
                    return rollback('invalid question data:', str(question_json))

        else:
            return rollback('invalid test data:', str(params_json))

        # transaction.set_rollback(True) # отключил транзакцию для тестов
        return HttpResponse("Test add sucsessfull")

    except JSONDecodeError:
        return rollback('invalid stream params to JSON: ', str(request.body))

    except Exception as E:
        transaction.set_rollback(True)
        return HttpResponseServerError(E)


def constructor_get(request, test_id):
    categorys = Category.objects.all()
    data = {}
    data['categorys'] = {}
    for category in categorys:
        data['categorys'][category.name] = {'name': category.name, 'selected': False}
        
    if test_id is None:
        return render(request, 'constructor.html', context={'data': data})
    else:
        test = Test.objects.get(id=test_id)

        if test.author != request.user:
            raise PermissionDenied

        questions = Question.objects.filter(test=test)

        data['test_id'] = test_id
        data['categorys'][test.category.name]['selected'] = True
        data['time'] = str(test.time)
        data['title'] = test.title
        data['description'] = test.description
        data['author'] = test.author.username
        data['questions'] = {}
        count_questions = 0
        count_answers = 0
        for i, question in enumerate(questions):
            count_questions += 1
            data['questions'][f'{i + 1}'] = {'question': question.question, 'multiple_ans': question.multiple_ans,
                                             'answers': {}}
            answers = Answer.objects.filter(question=question)
            for j, answer in enumerate(answers):
                count_answers += 1
                data['questions'][f'{i + 1}']['answers'][f'{i}_{j}'] = {'answer': answer.answer,
                                                                        'right_answer': answer.right_answer}

        data['count_questions'] = count_questions
        data['count_answers'] = count_answers
        return render(request, 'constructor.html', context={'data': data})


# Create your views here.

@login_required(login_url='login')
def constructor(request, test_id=None):
    if request.method == 'POST':
        return constructor_post(request, test_id)
    elif request.method == 'GET':
        return constructor_get(request, test_id)

    # return render(request, 'get_tocken.html') получение токена для postman


def contructor_result(request, test_id=None):
    return render(request, 'constructor_result.html', context={'test_id': test_id})
