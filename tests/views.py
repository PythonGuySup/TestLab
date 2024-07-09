from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.shortcuts import render
from django.conf import settings
from django.db import transaction
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError, HttpResponseForbidden
from tests.forms import ValidTest, ValidQuestion, ValidAnswer
from tests.models import Test, Question, Category, Answer
from datetime import datetime
from json import JSONDecodeError, loads


def error_500_view(request, exception):
    return render(request, '500.html')


def error_410_view(request, exception):
    return render(request, '410.html')


def error_409_view(request, exception):
    return render(request, '409.html')


def error_404_view(request, exception):
    return render(request, '404.html')


def error_403_view(request, exception):
    return render(request, '403.html')


def error_401_view(request, exception):
    return render(request, '401.html')


def error_400_view(request, exception):
    return render(request, '400.html')


def error_304_view(request, exception):
    return render(request, '304.html')


def error_204_view(request, exception):
    return render(request, '204.html')


def error_201_view(request, exception):
    return render(request, '201.html')


def error_200_view(request, exception):
    return render(request, '200.html')


def test_detail(request, test_id):
    test = Test.objects.get(pk=test_id)
    return render(request, 'test_detail.html', {'test': test})


def test_questions(request, test_id):
    if request.method == 'POST':
        print(request.POST)
    test = Test.objects.get(id=test_id)
    questions_list = Question.objects.filter(test=test)
    paginator = Paginator(questions_list, settings.QUESTIONS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'test': test,
        'page_obj': page_obj
    }

    return render(request, 'test_questions.html', context)


def test_result(request, test_id):
    test = Test.objects.get(id=test_id)
    return render(request, 'test_result.html', {'test': test})


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
    return HttpResponseBadRequest(message, str(details))


@transaction.atomic
def constructor_post(request, test_id):
    print(test_id)
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
                            return rollback('invalid answer data:' + str(answer_json))

                    if not count_right:
                        return rollback(
                            'At least one answer must be correct:' + str(question_form.cleaned_data['answers']))
                    elif question_form.cleaned_data['multiple_ans'] and count_right < 2:
                        return rollback(
                            'You must provide at least 2 correct answers:' + str(question_form.cleaned_data['answers']))
                    elif not question_form.cleaned_data['multiple_ans'] and count_right >= 2:
                        return rollback(
                            'You must specify only 1 correct answer:' + str(question_form.cleaned_data['answers']))
                else:
                    return rollback('invalid question data:' + str(question_json))

        else:
            return rollback('invalid test data:' + str(params_json))

        # transaction.set_rollback(True) # отключил транзакцию для тестов
        return HttpResponse("Test add sucsessfull")

    except JSONDecodeError:
        return rollback('invalid stream params to JSON: ' + str(request.body))

    except Exception as E:
        transaction.set_rollback(True)
        return HttpResponseServerError(E)


def constructor_get(request, test_id):
    if test_id is None:
        return render(request, 'constructor.html')
    else:
        data = {}
        test = Test.objects.get(id=test_id)

        if test.author != request.user:
            raise PermissionDenied

        questions = Question.objects.filter(test=test)

        data['test_id'] = test_id
        data['category'] = test.category.name
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
